#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

from pyswip import Prolog, prolog
from tinydb import TinyDB
from jsonschema import validate, ValidationError, SchemaError


class Pena:
    def __init__(self, questions, database):
        # Validate questions
        try:
            questions_schema = {
                "type": "array",
                "items": [
                    {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string"
                            },
                            "text": {
                                "type": "string"
                            }
                        },
                        "required": ["name", "text"]
                    }
                ]
            }
            validate(questions, questions_schema)
            self.questions = questions
        except (ValidationError, SchemaError):
            print "'questions' is not valid"
            raise TypeError()

        # Validate database instance
        if isinstance(database, TinyDB):
            self.database = database
        else:
            print "'database' is not valid"
            raise TypeError()

        # Generate rules from questions
        self.rules = []
        for index in range(len(self.questions)):
            rule = str(self.questions[index]['name']) \
                    + "(Character) :- character(Character, "
            for prev_arg in range(1, index+1):
                rule += "_, "
            rule += "true, "
            for next_arg in range(index+1, len(self.questions)):
                rule += "_, "
            rule = rule[:-2]
            rule += ")"

            # rule_not to query for characters for who
            # the rule is false
            rule_not = "not_" + str(self.questions[index]['name']) \
                + "(Character) :- character(Character, "
            for arg in range(len(self.questions)):
                rule_not += "_, "
            rule_not = rule_not[:-2]
            rule_not += "), not(" + str(self.questions[index]['name']) \
                        + "(Character))"

            self.rules.append(rule)
            self.rules.append(rule_not)

    def new_engine(self, facts, rules):
        p = Prolog()
        for fact in facts:
            p.assertz(str(fact))
        for rule in rules:
            p.assertz(str(rule))
        return p

    def process(self, answers, operation, limit=None):
        # Return variables initialisation
        decision = 'UNKNOWN'
        data = {}

        # Validate characters
        try:
            characters = self.database.all()
            possible_properties = {}
            possible_properties['name'] = {
                "type": "string"
            }
            for question in self.questions:
                possible_properties[question['name']] = {
                    "type": "boolean"
                }
            characters_schema = {
                "type": "array",
                "items": [
                    {
                        "type": "object",
                        "properties": possible_properties,
                        "required": ["name"]
                    }
                ]
            }
            validate(characters, characters_schema)
        except (ValidationError, SchemaError):
            data['exception'] = "'database.all()' is not valid"
            return decision, data

        # Validate answers JSON
        try:
            possible_questions = {}
            for question in self.questions:
                possible_questions[question['name']] = {
                    "type": "boolean"
                }

            answers_schema = {
                "type": "object",
                "properties": possible_questions
            }
            validate(answers, answers_schema)
        except (ValidationError, SchemaError):
            data['exception'] = "'answers' is not valid"
            return decision, data

        # Validate operation
        if operation != 'ASK' and operation != 'TELL':
            data['exception'] = "'operation' is not valid"
            return decision, data

        # Validate limit
        if operation == 'ASK':
            try:
                limit = int(limit)
                limit_schema = {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": len(self.questions)
                }
                validate(limit, limit_schema)
            except (ValidationError, SchemaError, ValueError, TypeError):
                data['exception'] = \
                    "'limit' should be an integer between 1 and " \
                    + str(len(self.questions))
                return decision, data

        # Generate facts from characters
        facts = []
        for character in characters:
            fact = "character('" + str(character['name']) + "', "
            # Every fact should have the exact same number
            # of answers as the number of questions
            # If the question has no answer write null
            for index in range(len(self.questions)):
                if self.questions[index]['name'] in character:
                    if character[self.questions[index]['name']]:
                        fact += "true, "
                    else:
                        fact += "false, "
                else:
                    fact += "null, "
            fact = fact[:-2]
            fact += ")"

            facts.append(fact)

        if operation == 'ASK':
            # Generate query from answers
            valid_answsers = {}
            remaining_questions = []
            query = "character(Character, "
            for index in range(len(self.questions)):
                question_name = self.questions[index]['name']
                if question_name in answers:
                    valid_answsers[question_name] = answers[question_name]
                    if answers[question_name]:
                        query += "true, "
                    else:
                        query += "false, "
                else:
                    query += "_, "
                    remaining_questions.append(self.questions[index])
            query = query[:-2]
            query += ")"

            # Run query
            try:
                p = self.new_engine(facts, self.rules)
                query_result = list(p.query(query))
            except prolog.PrologError:
                query_result = []
                data['exception'] = "Failed running 'query'"

            # Decide
            if len(valid_answsers) >= len(self.questions) \
                    or len(valid_answsers) >= limit:
                if query_result:
                    decision = 'FOUND'
                    data['character_found'] = (
                        query_result[
                            randint(0, len(query_result)-1)
                        ]['Character']
                    )
                else:
                    decision = 'NOTFOUND'
            else:
                decision = 'CONTINUE'
                data['next_question'] = remaining_questions[
                                            randint(
                                                0, len(remaining_questions)-1
                                            )
                                        ]
        elif operation == 'TELL':
            # Load valid answers
            valid_answsers = {}
            if 'name' in answers:
                valid_answsers['name'] = answers['name']
            for index in range(len(self.questions)):
                question_name = self.questions[index]['name']
                if question_name in answers:
                    valid_answsers[question_name] = answers[question_name]

            # Decide
            data = valid_answsers
            if 'name' in valid_answsers \
                    and valid_answsers['name'] != "" \
                    and len(valid_answsers) > 0:
                self.database.insert(valid_answsers)
                decision = 'ACCEPTED'
            else:
                decision = 'REJECTED'

        return decision, data

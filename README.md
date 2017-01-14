# PENA's an Entirely New Akinator

PENA is a game based on Twenty Questions that attempts to determine which character the player is thinking of by asking them a series of questions.

## Help for Windows

### Prerequisites

* Install python-2.7.13.msi

* Install swipl-w32-723.exe

* Execute the command prompt (cmd) as administrator and run:

```
rename "C:\Program Files (x86)\swipl\bin\libswipl.dll" libpl.dll
```

### Installing pena cli

* [Open a new command prompt](http://www.howtogeek.com/howto/windows-vista/stupid-geek-tricks-open-a-command-prompt-from-the-desktop-right-click-menu/) in PENA's root directory

```
python setup.py install
```

### Building PENAJavaLayer's WAR

* [Open a new command prompt](http://www.howtogeek.com/howto/windows-vista/stupid-geek-tricks-open-a-command-prompt-from-the-desktop-right-click-menu/) in PENA's root directory

```
cd pena_java_layer
set PATH=..\gradle\bin;%PATH%
gradle war
```

* The final WAR file location is: PENA_ROOT_DIRECTORY\pena_java_layer\build\libs\pena_java_layer.war

* Before deploying the WAR in your web server, make sure pena cli is running.

### Running pena cli 

* [Open a new command prompt](http://www.howtogeek.com/howto/windows-vista/stupid-geek-tricks-open-a-command-prompt-from-the-desktop-right-click-menu/) in PENA's root directory

```
set PATH=C:\Program Files (x86)\swipl\bin;%PATH%
pena questions_sample.json database.json localhost 5000
```

* "http://localhost:5000" is hardcoded in PenaJavaLayer so keep it as it is.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

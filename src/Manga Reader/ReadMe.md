
<h1 align='center'> <img width=32 src='icon.ico'> Manga Reader</h1>
<p align='center'>
    <img src='../../_img/manga_reader.PNG'><br>
    Manga Reader
</p>

## Synopsis

The most simplest Manga app there is, no CBR, no ZIP files needed, just your internet connection and a python interpreter ;)

## Installation

Install the [requirements](#requirements)
```bash
pip install bs4
pip install PySide6
pip install qtmodern
pip install requests
```

## Download

Click here to [Download Manga Reader](https://downgit.github.io/#/home?url=https://github.com/besnoi/pyapps/tree/main/src/Manga%20Reader)

## Requirements
- bs4
- PySide6
- qtmodern
- requests

## Caveats

<p align='justify'>
The app uses threads in a smart way to keep load images asynchronously. However killing threads takes time so user will have to double-click on a chapter <em>twice</em> if another chapter is being loaded - first time to stop loading the current chapter and second time to load the chapter the user wants the app to load. 

Also when a chapter is being loaded the docked tree widget's width is changed dynamically which looks more of a bug than a feature 

Finally, you can't resize the window, only current size and fullscreen thanks to `qtmodern` creators who still haven't implemented the functionality

Contributions to solve these issues are always welcome, maybe if I get some divine inspiration I could solve 'em myself, but do check on the code once
</p>

## License

See [LICENSE](https://github.com/besnoi/pyApps/blob/main/LICENSE) for more information

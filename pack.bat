pyinstaller ^
    --noconfirm ^
    --clean ^
    --windowed ^
    --icon=ico.ico ^
    --distpath .\dist ^
    --workpath .\build ^
    --specpath . ^
    --add-data ".\dll\*;." ^
    main.py
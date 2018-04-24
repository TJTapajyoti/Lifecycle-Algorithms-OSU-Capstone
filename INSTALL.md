# Install MSYS2 and GTK+

Go to the following link: https://www.gtk.org/download/windows.php

Follow the instructions, and do the optional Step 4, installing the Python 2 bindings.

Run the following commands:

```
pacman -S mingw-w64-x86_64-python2-pip
pacman -S mingw-w64-x86_64-python2-numpy
pacman -S git
git clone https://github.com/cheshyre/Lifecycle-Algorithms-OSU-Capstone
cd Lifecycle-Algorithms-OSU-Capstone/Updated\ SPA\ code/
```

Run the code with:
```
python alpha.py
```



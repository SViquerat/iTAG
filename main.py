# -*- coding: UTF-8 -*-

from lib.iTagLogic import *
from lib.defineGlobalParameters import *


def main():
    root = Tk()
    app = iTag(root, setGLOBALS())
    app.mainloop()


if __name__ == "__main__":
    main()

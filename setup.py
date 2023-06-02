from cx_Freeze import setup, Executable
  
setup(name = "newscraper" ,
      version = "2.0.0" ,
      description = "NEW GUI!!!" ,
      executables = [Executable("newscraper.py")])

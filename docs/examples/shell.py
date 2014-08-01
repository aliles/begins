import shutil
import begin

begin.subcommand(shutil.copy)
begin.subcommand(shutil.copy2)
begin.subcommand(shutil.copyfile)
begin.subcommand(shutil.copymode)
begin.subcommand(shutil.copystat)
begin.subcommand(shutil.copytree)
begin.subcommand(shutil.move)
begin.subcommand(shutil.rmtree)

# Patch in doc before the func is wrapped by begin.start
def patch_doc(doc):
   def decorate(func):
       func.__doc__ = doc
       return func
   return decorate

@begin.start
@patch_doc(shutil.__doc__)
def main():
   pass

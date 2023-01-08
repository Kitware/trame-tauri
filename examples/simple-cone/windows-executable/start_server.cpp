#include <cstdlib>
#include <string>
#include <Windows.h>

std::string GetCurrentDirectory()
{
  // Get the path to this executable
  char buffer[MAX_PATH];
  GetModuleFileNameA(NULL, buffer, MAX_PATH);
  std::string::size_type pos = std::string(buffer).find_last_of("\\/");

  return std::string(buffer).substr(0, pos);
}

int main(int argc, char* argv[])
{
  // Run the server.exe executable, and forward all arguments to it.
  // We must put it in quotes in case the path includes spaces.
  std::string cmd = "\"" + GetCurrentDirectory() + "\\server\\server.exe\"";

  // Now add in all the arguments
  for (int i = 1; i < argc; ++i) {
    cmd += " ";
    cmd += argv[i];
  }

  return system(cmd.c_str());
}

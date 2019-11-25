#include <iostream>     // std::cout
#include <fstream>      // std::ifstream

using namespace std;

int main () 
{
    for (size_t i = 0; i < 10000; i++)
    {
        ifstream ifs;

        ifs.open ("fichier", ifstream::in);

        char c = ifs.get();

        while (ifs.good()) 
        {
            //cout << c;
            c = ifs.get();
        }

        ifs.close();
    }
    

    return 0;
}
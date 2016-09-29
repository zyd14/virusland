#include <iostream>
#include "string.h"
#include <vector>
#include <cstring>
#include <fstream>
#include <stdlib.h>

using namespace std;
// must pass in all_files.txt FIRST then GKB_taxonomy.txt
int main(int argc, char *argv[])
{
    cout << "Creating taxonomy index" << endl;
    char * all_files = argv[1];
    char *file_name=new char [500];
    int j;
    string junk;

    ifstream in;
    ofstream out;
    out.open(argv[2]);

    vector <std::string> file_names;

    cout << "Opening " << all_files << endl;
    in.open(all_files);
    if (in.is_open()){
        while(in.peek()!=EOF)
            {
                getline(in,junk,'\n');
                file_names.push_back(junk);          
            }
        cout << "Done with while loop" << endl;
        in.clear();
        in.close();
    }
    else{ cout << "File not opened" << endl;}

    cout << "Start compiling genomes" << endl;

    int jj = 1;
    for (j = 0; j < file_names.size(); j++){

        in.open(file_names[j].c_str());
        if(!in.is_open()) {cout << "cannot find file " << jj<< "" << file_name << endl; jj++; continue;}

        getline(in,junk,'\n');
        string token = "ORGANISM";
        bool next_file = false;
        while (in.peek()!=EOF && next_file==false){
            getline(in,junk,'\n');

            string z = junk;
            size_t found = z.find(token);
            if (found!=std::string::npos){
                    string temp;
                    vector <string> fields;
                    int pos = found+token.length()+1;
                    temp = z.substr(pos, z.length()-1); // get first field, organism species
                    fields.push_back(temp);
                    temp="";

                    getline(in,junk,'\n');

                    z=junk;
                    int counter = 0;
                    while (z[counter]==' ') // strip junk spaces
                        counter ++;
                    for (int j = counter; j<z.length(); j++){
                        if (z[j]!=';' && z[j]!='.')
                            temp+=z[j];
                        else {fields.push_back(temp); temp="";}

                    }
                    //changed!!!
                   // out<<fields[0]<<"\t";
                    for (int i =0; i<fields.size(); i++){
                        out<<fields[i]<<"\t";
                    }
                    //out<<fields[1]<<endl;
                    out << "\n";
                    fields.clear();
                    found = std::string::npos;
                    next_file = true;
                    in.close();
                    in.clear();


            }
        }
    } out.clear(); out.close();
}

#include <iostream>
#include <vector>
#include <cstring>
#include <fstream>
#include <iostream>
#include <string>
#include <stdlib.h>

//TaxonomyXGenomeHits
//Takes Krona stats from CParser and output from TaxFromGBK

using namespace std;
 struct node{
        string taxonomy;
        double percent_hit;
        int num_hits;
        //num_hits=0;

};

int main(int argc, char *argv[])
{
    char * genome_stats;
    char * taxonomy;
    int i=0;
    string output;
    taxonomy=argv[1]; // taxonomy NEEDS to be first command line arg
    genome_stats=argv[2];
    output=argv[3];
    /*if (argc==1){
        genome_stats = "/home/lsb456/virusLand2/src/Krona_statsStuff"; //Stats code from Catherine's parser
        taxonomy="/home/lsb456/virusLand/TaxFromGBK/GBK_Taxonomy2.txt";
    }
    else{
        taxonomy=argv[1]; // taxonomy NEEDS to be first command line arg
        genome_stats=argv[2];
        output=argv[3]
    }*/
    ifstream oddish;
    double threshold = 5;
    char  junk [500];

    vector <node> viruses;
    cout<<"Reading Taxonomy"<<endl;
    oddish.open(taxonomy);
    if (!oddish.is_open()){cout<<"Unable to find taxonomy"<<endl; return 0;}
    while (oddish.peek()!=EOF){

        node temp;
	temp.num_hits=0;
        oddish.getline(junk, 500, '\n');
        temp.taxonomy = junk;
        viruses.push_back(temp); // create data structure of each virus from taxonomy generator
	i++;
    }
    cout<<"Reading Stats"<<endl;
    oddish.clear();
    oddish.close();
    oddish.open(genome_stats);
    if (!oddish.is_open()){cout<<"Unable to find statistics"<<endl; return 0;}

    oddish.getline(junk, 500, '\n'); // strip header

    char * virus_name;
    char * hits_to_genome;
    char * percent_proteins_hit;


    while(oddish.peek()!=EOF){
        oddish.getline(junk, 100, '\t');
        oddish.getline(junk, 100, '\t'); // get virus name
        virus_name=new char[strlen(junk)+1];
        sprintf(virus_name,"%s",junk);
        oddish.getline(junk, 100, '\t');
        oddish.getline(junk, 100, '\t'); // get hits to genome
        hits_to_genome=new char[strlen(junk)+1];
        sprintf(hits_to_genome,"%s",junk);
        oddish.getline(junk, 100, '\n'); // get percent proteins hit, end of line
        percent_proteins_hit=new char[strlen(junk)+1];
        sprintf(percent_proteins_hit,"%s",junk);
        for (int j = 0; j <viruses.size(); j++ ){ //search for current virus in taxonomy list
            string tax = viruses[j].taxonomy;
            size_t found = tax.find(virus_name);
            if (found!=std::string::npos){
                viruses[j].percent_hit = atoi(percent_proteins_hit);
                viruses[j].num_hits = atoi(hits_to_genome);
                break;
            }
        }
        delete virus_name;
        delete hits_to_genome;
        delete percent_proteins_hit;
    }


    oddish.clear();
    oddish.close();
    ofstream out;
    cout << "About to output file" << endl;
    //string output="/home/lsb456/virusLand2/src/TaxonomyXGenomeHits/";
    //output+=genome_stats;

    char * m = (char *) output.c_str();
    out.open(m); // output file name unique to genome_stats file name
    if (!out.is_open())
        cout<<"problem"<<endl;

    for(int i = 0; i <viruses.size(); i++){
        if (viruses[i].num_hits!=0)
            out<<viruses[i].num_hits<<viruses[i].taxonomy<<endl;
    }
    cout << "File should be out" << endl;
    out.clear();
    out.close();

    return 0;
}

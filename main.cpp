#include<iostream>
#include<bits/stdc++.h>
#include<map>
#include<string>
#include<vector>
#include<fstream>
#define ld double
using namespace std;
const ld INF = 1000000000;
int main(int argc, char** argv){
    string hh = argv[1];
    if(hh == "A"){ 
        map<string,ld> gatedelays;
        map<string,ld> nodedelay;
        map<string,ld> outputdelay;
        map<string,pair<vector<string>,ld>> nodeadj;
        vector<string> primaryinputs;
        vector<string> primaryoutputs;
        string gd = argv[3];
        ifstream in1(gd);
        while(!in1.eof()){
            string text;
            getline(in1, text);
            if((text.size()==0)){continue;}
            if((text[0]=='/') && text[1]=='/'){continue;}
            if((text[0]==' ')){continue;}
            vector<string> data;
            stringstream iss(text);
            while(iss>>text){
                data.push_back(text.c_str());
            }
            string init = data[0];
            for(int i = 0;i<data.size();i++){
                gatedelays[data[0]] = stold(data[1]);
            }     
        }
        string ckt = argv[2];
        ifstream in2(ckt);
        while(!in2.eof()){
            string text;
            getline(in2, text);
            if((text.size()==0)){continue;}
            if((text[0]=='/') && text[1]=='/'){continue;}
            if((text[0]==' ')){continue;}
            vector<string> data;
            stringstream iss(text);
            while(iss>>text){
                data.push_back(text.c_str());
            }
            int n = data.size();
            for(ld i = 1;i<data.size();i++){
                if(data[0] == "PRIMARY_INPUTS"){
                    primaryinputs.push_back(data[i]);
                }
                else if(data[0] == "PRIMARY_OUTPUTS"){
                    primaryoutputs.push_back(data[i]);
                    outputdelay[data[i]] = -1;
                }
                else if(data[0] == "INTERNAL_SIGNALS"){
                }
                else{
                    if(i==n-1){break;}
                    vector<string> a;
                    if(nodeadj.find(data[n-1])==nodeadj.end()){nodeadj[data[n-1]] = (make_pair(a,-1));}
                    nodeadj[data[n-1]].first.push_back(data[i]);
                    // cout<<nodeadj[data[n-1]].first.size()<<" ";
                    nodedelay[data[n-1]] = gatedelays[data[0]];
                }

            }     
            // f0r(i,data.size()){cout<<data[i][0]<<"";}cout<<endl; 
        }
        ld value = 0;
        function< ld (string)> run = [&](string node){
            value=0;
            if(find(primaryinputs.begin(), primaryinputs.end(), node) != primaryinputs.end()){
                ld zero = 0;
                return zero;
            }
            else if(nodeadj[node].second != -1){
                return nodeadj[node].second;
            }
            else{
                for(auto child : nodeadj[node].first){
                    nodeadj[node].second = max(nodeadj[node].second,run(child));
                }
                nodeadj[node].second+=nodedelay[node];
                return nodeadj[node].second;
            }
        };
        for(auto first : primaryoutputs){
            outputdelay[first] = run(first);
        }
        ofstream Myfile("output_delays.txt");
        for(auto first : primaryoutputs){
            cout.precision(17);
            Myfile<<first<<" "<<outputdelay[first]<<endl;
        }
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    else{
        map<string,ld> inputdelays;
        map<string,ld> gatedelays;
        map<string,ld> nodedelay;
        map<string,ld> desiredoutputdelay;
        map<string,pair<vector<string>,ld>> nodeadj;
        vector<string> primaryinputs;
        vector<string> primaryoutputs;
        string rd = argv[4];
        ifstream in(rd);
        while(!in.eof()){
            string text;
            getline(in, text);
            if((text.size()==0)){continue;}
            if((text[0]=='/') && text[1]=='/'){continue;}
            if((text[0]==' ')){continue;}
            stringstream iss(text);
            vector<string> data;
            while(iss>>text){
                data.push_back(text.c_str());
            }
            for(ld i = 0;i<data.size();i++){
                desiredoutputdelay[data[0]] = stold(data[1]);
            }
            // f0r(i,data.size()){cout<<data[i][0]<<"";}cout<<endl; 
        }
        string gd = argv[3];
        ifstream in1(gd);
        while(!in1.eof()){
            string text;
            getline(in1, text);
            if((text.size()==0)){continue;}
            if((text[0]=='/') && text[1]=='/'){continue;}
            if((text[0]==' ')){continue;}
            vector<string> data;
            stringstream iss(text);
            while(iss>>text){
                data.push_back(text.c_str());
            }
            string init = data[0];
            for(ld i = 0;i<data.size();i++){
                gatedelays[data[0]] = stold(data[1]);
            }     
            // f0r(i,data.size()){cout<<data[i][0]<<"";}cout<<endl; 
        }
        string ckt = argv[2];
        ifstream in2(ckt);
        while(!in2.eof()){
            string text;
            getline(in2, text);
            if((text.size()==0)){continue;}
            if((text[0]=='/') && text[1]=='/'){continue;}
            if((text[0]==' ')){continue;}
            vector<string> data;
            stringstream iss(text);
            while(iss>>text){
                data.push_back(text.c_str());
            }
            ld n = data.size();
            for(ld i = 1;i<data.size();i++){
                if(data[0] == "PRIMARY_INPUTS"){
                    primaryinputs.push_back(data[i]);
                    inputdelays[data[i]] = INF;
                }
                else if(data[0] == "PRIMARY_OUTPUTS"){
                    primaryoutputs.push_back(data[i]);
                }
                else if(data[0] == "INTERNAL_SIGNALS"){
                }
                else{
                    if(i==n-1){break;}
                    vector<string> a;
                    if(nodeadj.find(data[i])==nodeadj.end()){nodeadj[data[i]] = (make_pair(a,INF));}
                    nodeadj[data[i]].first.push_back(data[n-1]);
                    // cout<<nodeadj[data[i]].first.size()<<endl;
                    nodedelay[data[n-1]] = gatedelays[data[0]];
                }

            }     
            // f0r(i,data.size()){cout<<data[i][0]<<"";}cout<<endl; 
        }
        function< ld (string)> run = [&](string node){
            if(find(primaryoutputs.begin(), primaryoutputs.end(), node) != primaryoutputs.end()){
                ld zero = desiredoutputdelay[node]-nodedelay[node];
                return zero;
            }
            else if(nodeadj[node].second != INF){
                return nodeadj[node].second;
            }
            else{
                for(auto child : nodeadj[node].first){
                    nodeadj[node].second = min(nodeadj[node].second,run(child));
                }
                nodeadj[node].second-=nodedelay[node];
                return nodeadj[node].second;
            }
        };
        for(auto node : primaryinputs){
            for(auto child : nodeadj[node].first){
                inputdelays[node] = min(inputdelays[node],run(child));
            }
        }
        ofstream Myfile2("input_delays.txt");
        for(auto first : primaryinputs){
            Myfile2.precision(7);
            Myfile2<<first<<" "<<inputdelays[first]<<endl;
        }
    }
}
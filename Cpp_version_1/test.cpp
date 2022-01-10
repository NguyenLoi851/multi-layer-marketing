// // // #include<iostream>
// // // #include<fstream>
// // // #include<vector>
// // // #include<sstream>
// // // using namespace std;

// // // int main(){
// // //     // ofstream fs;
// // //     // fs.open("test.csv", ios::app | ios::ate);
// // //     // fs << "Hello" << endl << "I'm Loi";
// // //     // fs.close();
// // //     vector<vector<string>> content;
// // // 	vector<string> row;
// // // 	string line, word;
 
// // // 	ifstream fs;
// // //     fs.open("test.csv");
// // //     if(fs.is_open()){
// // //         // getline(fs,line);
// // //         // if(line != "")
// // //         // cout << line;
// // //         // else cout << "gg";
// // //         // getline(fs,line);
// // // 		while(getline(fs, line))
// // // 		{
// // // 			row.clear();
 
// // // 			stringstream str(line);
 
// // // 			// while(getline(str, word, ','))
// // // 			// 	row.push_back(word);
// // //             getline(str,word,',');
// // //             row.push_back(word);
// // //             getline(str,word,',');
// // //             if(word !="") row.push_back(word);
// // //             else row.push_back("x");
// // // 			content.push_back(row);
// // // 		}
// // //     }else{
// // //         cout<<"Could not open the file\n";
// // //     }
// // //     for (int i=0;i<content.size();i++){
// // //         for (int j=0;j<content[i].size();j++){
// // //             cout << content[i][j] << " ";
// // //         }
// // //         cout << endl;
// // //     }

// // //     return 0;
// // // }

// // #include<iostream>
// // #include<fstream>
// // using namespace std;

// // int main(){
// //     // fstream fs;
// //     // string line;
// //     // fs.open("test.csv",ios::app|ios::ate);
// //     // fs << 1 << "," << 2 << endl;
// //     // cout << fs.tellp() << endl;
// //     // fs.seekp(20,ios::beg);
// //     // cout << fs.tellp() << endl;
// //     // getline(fs,line);
// //     // if(line == "") cout << "gg";
// //     // else cout << line;
// //     // fs.close();

// //     ifstream fs;
// //     fs.open("test.csv");
// //     if(fs.is_open()){
// //         string line;
// //         getline(fs,line);
// //         cout << stoi(line,nullptr,10);
// //         fs.close();
// //     }else{
// //         cout << "Cannot open file";
// //     }

// //     return 0;
// // }

// // #include<iostream>
// // using namespace std;

// // int function(int x){
// //     return x+2;
// // }

// // int main(){
// //     int x=3;
// //     x = function(x);
// //     cout << x;
// //     return 0;
// // }

// #include<iostream>
// #include<fstream>
// using namespace std;

// int main(){
//     fstream fs;
//     fs.open("test.csv", ios::out|ios::in);
//     if(fs.is_open()){
//         string line;
//         getline(fs, line);
//         cout << line;
//         fs << "hh";
//         fs.close();
//     }else{
//         cout << "No";
//     }

//     return 0;
// }

#include<iostream>
#include<map>
using namespace std;

struct Sale{
    int id;
    float ss;
};

typedef struct Sale Sale;

Sale *create(int id, float ss){
    Sale *tmp = new Sale;
    tmp->id = id;
    tmp->ss = ss;
    return tmp;
}

int main(){
    map<int, Sale*> m;
    Sale *a = create(1,2);
    Sale *b = create(3,4);
    m[1] = a;
    m[2] = b;
    cout << m[1]->id << endl;
    cout << m[2]->ss << endl;
    // cout << m[3]->id << endl;
    if(m[3] == NULL) cout << "gg" << endl;
    cout << m[1]->ss << endl;
    return 0;
}
#include<iostream>
#include<fstream>
#include<string>
#include<sstream>
using namespace std;

struct Distributor{
    int id;
    string name;
    struct Distributor *left;
    struct Distributor *right;
    struct Distributor *parent;
};

typedef struct Distributor Distributor;

Distributor* createDistributor(int id, string name){
    Distributor* newDistributor = NULL;
    newDistributor = new Distributor;
    if (newDistributor == NULL){
        cout << "Out of memory" << endl;
        exit(1);
    }else{
        newDistributor->left = NULL;
        newDistributor->right = NULL;
        newDistributor->parent = NULL;
        newDistributor->id = id;
        newDistributor->name = name;
    }
    return newDistributor;
}

Distributor* findDistributorById(Distributor *root, int id){
    Distributor *tempDistributor = NULL;
    if(root->id == id) return root;
    if(root->left == NULL && root->right == NULL) return NULL;
    if(root->left != NULL){
        tempDistributor = findDistributorById(root->left,id);
    }
    if(tempDistributor != NULL) return tempDistributor;
    else{
        if(root->right != NULL){
            tempDistributor = findDistributorById(root->right,id);
        }
    }
    return tempDistributor;
    
}

Distributor* insertDistributor(Distributor *root, int id, string name, int parentId){

    Distributor *newDistributor;
    newDistributor = createDistributor(id, name);
    if(root == NULL){
        ofstream fs;
        fs.open("Distributor.csv",ios::app|ios::ate);
        if(fs.is_open()){
            fs << newDistributor->id << "," << newDistributor->name << "," << endl;
            fs.close();
        }else{
            cout << "Cannot open file Distributor.csv" << endl;
        }
        return newDistributor;
    }
    Distributor *parentDistributor = findDistributorById(root, parentId);
    if(parentDistributor->left == NULL && parentDistributor->right == NULL){
        if(rand()%2 == 1){
            parentDistributor->left = newDistributor;
        }else{
            parentDistributor->right = newDistributor;
        }
        newDistributor->parent = parentDistributor;
    }else if(parentDistributor->left == NULL){
        parentDistributor->left = newDistributor;
        newDistributor->parent = parentDistributor;
    }else if(parentDistributor->right == NULL){
        parentDistributor->right = newDistributor;
        newDistributor->parent = parentDistributor;
    }else{
        delete newDistributor;
        if(rand()%2 == 1){
            root->left = insertDistributor(root->left, id, name, root->left->id);
        }else{
            root->right = insertDistributor(root->right, id, name, root->right->id);
        }
    }
    //save to database
    ofstream fs;
    fs.open("Distributor.csv",ios::app|ios::ate);
    if(fs.is_open()){
        fs << newDistributor->id << "," << newDistributor->name << "," << newDistributor->parent->id << endl;
        fs.close();
    }else{
        cout << "Cannot open file Distributor.csv" << endl;
    }

    return root;
}

Distributor *getAllDistributor(ifstream &fs){
    int id, parentId;
    string name;
    Distributor *root = NULL;
    string line, word;
    getline(fs, line);
    while(getline(fs,line)){
        stringstream str(line);
        getline(str,word,',');
        id = stoi(word,nullptr,10);
        getline(str,word,',');
        name = word;
        getline(str,word,',');
        if(word != "") parentId = stoi(word,nullptr,10);
        if(root == NULL){
            root = insertDistributor(root, id, name, 0);
        }else{
            root = insertDistributor(root, id, name, parentId);
        }
    }
    return root;
}

int main(){
    Distributor *root = NULL;
    bool fileStatus; //false: NULL, true: Has data
    ifstream fs;
    fs.open("Distributor.csv");
    if(fs.is_open()){
        string line;
        getline(fs,line);
        if(line == ""){
            fileStatus = false;
        }else{
            fileStatus = true;
        }
        fs.close();
    }else{
        cout << "Cannot open file Distributor" << endl;
    }
    
    if(fileStatus == false){ // Start write to file
        ofstream fs;
        fs.open("Distributor.csv",ios::app|ios::ate);
        if(fs.is_open()){
            fs << "Id,Name,ParentId" << endl;
            fs.close();
        }else{
            cout << "Cannot open file Distributor";
        }
    }else{ // Get data of file
        int id, parentId;
        string name;
        string temp;
        ifstream fs;
        string line;
        fs.open("Distributor.csv",ios::in);
        if(fs.is_open()){
            root = getAllDistributor(fs);
            fs.close();
        }else{
            cout << "Cannot open file Distributor";
        }
    }

    while(true){
        cout << endl;
        cout << " =======================================================" << endl;
        cout << " =====  Please select function by key 1,2,3,4      =====" << endl;
        cout << " =====  1. Enter new distributor information       =====" << endl;
        cout << " =====  2. Delete distributor information          =====" << endl;
        cout << " =====  3. Enter sales information                 =====" << endl;
        cout << " =====  4. Exit the program                        =====" << endl;
        cout << " =======================================================" << endl;
        cout << " >> Select function: " ;
        char selectFunc;
        cin >> selectFunc;
        if(isdigit(selectFunc) == false){
            cout << "\n <!><!> Select again from key 1 to 4 <!><!>" << endl;
            continue;
        }else if(selectFunc=='4'){
            break;
        }else{
            switch (selectFunc-'0'){
                case 1:{
                    // enter infor
                    int id, parentId;
                    string name;
                    if (root == NULL){
                        cout << "Enter information of highest distributor" << endl;
                        cout << "Enter id: ";
                        cin >> id;
                        cout << "Enter name: ";
                        cin >> name;
                        root = insertDistributor(root, id, name,0);
                    }else{
                        cout << "Enter information of new distributor" << endl;
                        cout << "Enter id: ";
                        cin >> id;
                        if(findDistributorById(root, id) != NULL){
                            cout << "Id existed, Enter other id" << endl;
                        }
                        cout << "Enter name: ";
                        cin >> name;
                        cout << "Enter parentId: ";
                        cin >> parentId;
                        if(findDistributorById(root, parentId) == NULL){
                            cout << "ParentId doesn't exist, Enter other parentId" << endl;
                        }
                        root = insertDistributor(root, id, name, parentId);
                    }
                    break;
                }
                case 2:{
                    //Function 2;
                    break;
                }
                case 3:{
                    //Function 3;
                    break;
                }
                default:{
                    cout << "\n <!><!> Select again from key 1 to 4 <!><!>" << endl;
                    break;
                }
                
            }
        }

        char text;
        cout << " >> Continue [any key] or exit program [q||Q]: ";
        if (text == 'q' || text == 'Q'){
            break;
        }
    }
    return 0;
}
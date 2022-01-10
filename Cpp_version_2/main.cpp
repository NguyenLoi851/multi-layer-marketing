#include<iostream>
#include<fstream>
#include<string>
#include<sstream>
#include<map>
using namespace std;

struct Distributor{
    int id;
    string name;
    struct Distributor *left;
    struct Distributor *right;
    struct Distributor *parent;
};

struct Sale{
    int batch;
    int id;
    float sales;
    float commission;
};

typedef struct Distributor Distributor;

typedef struct Sale Sale;

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

Distributor* createDistributor(int id, string name){
    Distributor* newDistributor = NULL;
    newDistributor = new Distributor;
    if (newDistributor == NULL){
        cout << endl << "Out of memory" << endl;
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

Sale *createSale(int batch, int id, float sales, float commission){
    Sale *distributorSale = NULL;
    distributorSale = new Sale;
    if (distributorSale == NULL){
        cout << endl << "Out of memory" << endl;
        exit(1);
    }else{
        distributorSale->batch = batch;
        distributorSale->id = id;
        distributorSale->sales = sales;
        distributorSale->commission = commission;
    }
    return distributorSale;
}

Sale *getDistributorSale(Distributor *root){
    Sale *distributorSale;
    string line, word;
    float sales, commission;
    int batch;
    ifstream fs;
    fs.open("Number Of Batch Sale.csv");
    if(fs.is_open()){
        getline(fs,line);
        batch = stoi(line,nullptr,10);
        fs.close();
    }else{
        cout << endl << "Cannot open file Number Of Batch Sale.csv" << endl;
    }
    ifstream saleFile;
    saleFile.open("Sales.csv");
    getline(saleFile,line);
    if(saleFile.is_open()){
        while(getline(saleFile,line)){
            stringstream str(line);
            getline(str,word,',');
            if(stoi(word,nullptr,10) != batch)
                continue;
            getline(str,word,',');
            if(stoi(word,nullptr,10) != root->id)
                continue;
            getline(str,word,',');
            sales = stof(word,nullptr);
            getline(str,word,',');
            commission = stof(word,nullptr);
            break;
        }
        distributorSale = createSale(batch, root->id, sales, commission);
    }else{
        cout << endl << "Cannot open file Sales.csv" << endl;
    }
    return distributorSale;
}

Distributor *insertDistributor(Distributor *parentDistributor, Distributor *newDistributor){
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
        if(rand()%2 == 1){
            newDistributor = insertDistributor(parentDistributor->left, newDistributor);
        }else{
            newDistributor = insertDistributor(parentDistributor->right, newDistributor);
        }
    }    
    return newDistributor;
}

Distributor *getAllDistributor(string fileName){
    Distributor *root = NULL;
    ifstream fs;
    fs.open(fileName,ios::in);
    if(fs.is_open()){
        Distributor *newDistributor, *parentDistributor;
        int id, parentId;
        string name;
        string line, word;
        getline(fs,line);
        while(getline(fs,line)){
            stringstream str(line);
            getline(str,word,',');
            id = stoi(word, nullptr, 10);
            getline(str,word,',');
            name = word;
            getline(str,word,',');
            if(word != ""){
                parentId = stoi(word, nullptr, 10);
                parentDistributor = findDistributorById(root, parentId);
                newDistributor = createDistributor(id, name);
                newDistributor = insertDistributor(parentDistributor, newDistributor);
            }else{
                root = createDistributor(id, name);
            }
        }
        fs.close();

    }else{
        cout << endl << "Cannot open file Distributor"<< endl;
    }    
    return root;
}

void addNewDistributorToDatabase(string fileName, Distributor *newDistributor){
    ofstream fs;
    fs.open(fileName, ios::app|ios::ate);
    if(fs.is_open()){
        if(newDistributor->parent != NULL){
            fs << newDistributor->id << "," << newDistributor-> name <<
            "," << newDistributor->parent->id << endl;
        }else{
            fs << newDistributor->id << "," << newDistributor-> name <<
            "," << "" << endl;
        }
        fs.close();
    }else{
        cout << endl << "Cannot open file Distributor" << endl;
    }    
}

Distributor *deleteDistributor(Distributor *delDistributor){
    Distributor *parentDistributor = delDistributor->parent;
    if(parentDistributor == NULL){// delete root
        if(delDistributor->left == NULL && delDistributor->right == NULL){
            delDistributor = NULL;
            delete delDistributor;
            return NULL;
        }else if(delDistributor->left == NULL){
            Distributor *tmpDistributor = delDistributor->right;
            tmpDistributor->parent = NULL;
            delete delDistributor;
            return tmpDistributor;
        }else if(delDistributor->right == NULL){
            Distributor *tmpDistributor = delDistributor->left;
            tmpDistributor->parent = NULL;
            delete delDistributor;
            return tmpDistributor;
        }else{
            string flag;
            Distributor *tmpDistributor;

            Sale *leftChildDistributorSale = getDistributorSale(delDistributor->left);
            Sale *rightChildDistributorSale = getDistributorSale(delDistributor->right);

            if(leftChildDistributorSale->commission > rightChildDistributorSale->commission){
                flag = "left";
            }else if(leftChildDistributorSale->commission < rightChildDistributorSale->commission){
                flag = "right";
            }else if(leftChildDistributorSale->sales > rightChildDistributorSale->sales){
                flag = "left";
            }else if(leftChildDistributorSale->sales < rightChildDistributorSale->sales){
                flag = "right";
            }else if(rand()%2 == 1){
                flag = "left";
            }else{
                flag = "right";
            }
            if(flag == "left"){
                tmpDistributor = createDistributor(delDistributor->left->id, delDistributor->left->name);
                tmpDistributor->right = delDistributor->right;
                tmpDistributor->right->parent = tmpDistributor;
                
                tmpDistributor->left = deleteDistributor(delDistributor->left);
                if(tmpDistributor->left != NULL)
                    tmpDistributor->left->parent = tmpDistributor;
                
                delete delDistributor;
                return tmpDistributor;
            }else{
                tmpDistributor = createDistributor(delDistributor->right->id, delDistributor->right->name);
                tmpDistributor->left = delDistributor->left;
                tmpDistributor->left->parent = tmpDistributor;
                
                tmpDistributor->right = deleteDistributor(delDistributor->right);
                if(tmpDistributor->right != NULL)
                    tmpDistributor->right->parent = tmpDistributor;
                
                delete delDistributor;
                return tmpDistributor;
            }
        }
    }else{
        if(delDistributor->left == NULL && delDistributor->right == NULL){ //delDistributor doesn't have any child
            if(parentDistributor->left == delDistributor){
                parentDistributor->left = NULL;
            }else{
                parentDistributor->right = NULL;
            }
            delete delDistributor;
            return NULL;
        }else if(delDistributor->left == NULL){ //delDistributor has only right child
            if(parentDistributor->left == delDistributor){
                parentDistributor->left = delDistributor->right;
                delDistributor->right->parent = parentDistributor;
                delete delDistributor;
                return parentDistributor->left;
            }else{
                parentDistributor->right = delDistributor->right;
                delDistributor->right->parent = parentDistributor;
                delete delDistributor;
                return parentDistributor->right;
            }
        }else if(delDistributor->right == NULL){ //delDistributor has only left child
            if(parentDistributor->left == delDistributor){
                parentDistributor->left = delDistributor->left;
                delDistributor->left->parent = parentDistributor; 
                delete delDistributor;
                return parentDistributor->left;
            }else{
                parentDistributor->right = delDistributor->left;
                delDistributor->left->parent = parentDistributor;
                delete delDistributor;
                return parentDistributor->right;
            }
        }else{ // delDistributor has 2 children
            string flag; // "left": choose left child, "right": choose right child
            Distributor *tmpDistributor;
            if(rand()%2 == 1){
                flag = "left";
            }else{
                flag = "right";
            }
            if(flag == "left"){
                tmpDistributor = createDistributor(delDistributor->left->id, delDistributor->left->name);
                if(parentDistributor->left == delDistributor){
                    parentDistributor->left = tmpDistributor;
                    tmpDistributor->parent = parentDistributor;

                    tmpDistributor->right = delDistributor->right;
                    delDistributor->right->parent = tmpDistributor;

                    tmpDistributor->left = deleteDistributor(delDistributor->left);
                    if(tmpDistributor->left != NULL)    
                        tmpDistributor->left->parent = tmpDistributor;

                    delete delDistributor;
                    return tmpDistributor;
                }else{
                    parentDistributor->right = tmpDistributor;
                    tmpDistributor->parent = parentDistributor;

                    tmpDistributor->right = delDistributor->right;
                    delDistributor->right->parent = tmpDistributor;

                    tmpDistributor->left = deleteDistributor(delDistributor->left);
                    if(tmpDistributor->left != NULL) 
                        tmpDistributor->left->parent = tmpDistributor;

                    delete delDistributor;
                    return tmpDistributor;                
                }
            }else{
                // alterDistributor = delDistributor->right;
                tmpDistributor = createDistributor(delDistributor->right->id, delDistributor->right->name);
                if(parentDistributor->left == delDistributor){
                    parentDistributor->left = tmpDistributor;
                    tmpDistributor->parent = parentDistributor;

                    tmpDistributor->left = delDistributor->left;
                    delDistributor->left->parent = tmpDistributor;

                    tmpDistributor->right = deleteDistributor(delDistributor->right);
                    if(tmpDistributor->right != NULL)
                        tmpDistributor->right->parent = tmpDistributor;

                    delete delDistributor;
                    return tmpDistributor;
                }else{
                    parentDistributor->right = tmpDistributor;
                    tmpDistributor->parent = parentDistributor;

                    tmpDistributor->left = delDistributor->left;
                    delDistributor->left->parent = tmpDistributor;

                    tmpDistributor->right = deleteDistributor(delDistributor->right);
                    if(tmpDistributor->right != NULL)
                        tmpDistributor->right->parent = tmpDistributor;

                    delete delDistributor;
                    return tmpDistributor;
                }
            }
        }
    }
}

void insertDistributorToDatabase(ofstream &fs, Distributor *root){
    if(root == NULL){
        return;
    }
    addNewDistributorToDatabase("Distributor.csv", root);
    insertDistributorToDatabase(fs, root->left);
    insertDistributorToDatabase(fs, root->right);
}

void updateDistributorDatabase(Distributor *root){
    ofstream fs;
    fs.open("Distributor.csv");
    if(fs.is_open()){
        fs << "Id,Name,ParentId" << endl;
        insertDistributorToDatabase(fs, root);   
        fs.close();     
    }else{
        cout << endl << "Cannot open file distributor" << endl;
    }
}

int countDistributor(Distributor *root){
    int cnt = 0;
    if(root == NULL) return 0;
    cnt = 1 + countDistributor(root->left) + countDistributor(root->right);
    return cnt;
}

float calculateCommission(Distributor *root, map<int,Sale*> &joinById){
    if(root == NULL){
        return 0;
    }
    float commission = 0;
    if(joinById[root->id] == NULL){
        Sale *distributorSale = createSale(joinById.begin()->second->batch, root->id, 0, 0);
        joinById[root->id] = distributorSale;
        commission = 0;
    }else{
        commission = 1.0*joinById[root->id]->sales / 10;
    }

    float leftChildDistributorCommission = calculateCommission(root->left, joinById);
    float rightChildDistributorCommission = calculateCommission(root->right, joinById);
    if(leftChildDistributorCommission > 0 && rightChildDistributorCommission > 0){
        if(leftChildDistributorCommission < rightChildDistributorCommission){
            if(leftChildDistributorCommission < 1.0*90/100*rightChildDistributorCommission){
                commission += leftChildDistributorCommission / 10;
            }else{
                commission += leftChildDistributorCommission / 10;
                commission += rightChildDistributorCommission / 10;
            }
        }else if(rightChildDistributorCommission < leftChildDistributorCommission){
            if(rightChildDistributorCommission < 1.0*90/100*leftChildDistributorCommission){
                commission += rightChildDistributorCommission / 10;
            }else{
                commission += leftChildDistributorCommission / 10;
                commission += rightChildDistributorCommission / 10;            
            }
        }else{
            commission += leftChildDistributorCommission / 10;
            commission += rightChildDistributorCommission / 10;          
        }
    }else if(leftChildDistributorCommission == 0 && rightChildDistributorCommission > 0){
        commission += rightChildDistributorCommission / 10;
    }else if(rightChildDistributorCommission == 0 && leftChildDistributorCommission > 0){
        commission += leftChildDistributorCommission / 10;
    }else{
        commission += 0;
    }

    joinById[root->id]->commission = commission;
    return commission;
}

void updateSaleDatabase(ofstream &fs, map<int, Sale*> joinById){
    for(auto &x: joinById){
        fs << x.second->batch << "," << x.second->id << "," 
        << x.second->sales << "," << x.second->commission << endl;
    }
}

void createFile(string fileName, string title){
    ofstream fs;
    fs.open(fileName,ios::app|ios::ate);
    if(fs.is_open()){
        fs << title << endl;
        fs.close();
    }else{
        cout << endl << "Cannot open file Distributor.csv"<< endl;
    }
}

int main(){
    Distributor *root = NULL;
    // Check status of file Distributor.csv: has data or not or doesn't exist
    bool fileStatus = false; //false: NULL / doesn't exist, true: has data
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
        cout << endl << " >> Cannot open file Distributor"<< endl;
    }

    if(fileStatus == false){ // Create and start write to file
        createFile("Distributor.csv", "Id,Name,ParentId");
    }else{ // Get data of file
        root = getAllDistributor("Distributor.csv");
    }

    while(true){
        cout << endl;
        cout << " =======================================================" << endl;
        cout << " =====  Please select function by key 1, 2, 3, 4   =====" << endl;
        cout << " =====  1. Enter new distributor information       =====" << endl;
        cout << " =====  2. Delete distributor information          =====" << endl;
        cout << " =====  3. Enter sales information                 =====" << endl;
        cout << " =====  4. Exit the program                        =====" << endl;
        cout << " =======================================================" << endl;
        cout << " >> Select function: " ;
        char selectFunc;
        cin >> selectFunc;
        if(isdigit(selectFunc) == false){
            cout << endl << " >> Select again from key 1 to 4"<< endl;
            continue;
        }else if(selectFunc=='4'){
            break;
        }else{
            switch (selectFunc-'0'){
                case 1:{ // Enter new distributor information
                    // Enter infor
                    int id, parentId;
                    string name;
                    Distributor *newDistributor = NULL;
                    if (root == NULL){
                        cout << endl << " >> Enter information of highest distributor";
                        cout << endl << " >> Enter id: ";
                        cin >> id;
                        cout << " >> Enter name: ";
                        cin >> name;
                        // create root
                        newDistributor = createDistributor(id, name);
                        root = newDistributor;
                    }else{
                        cout << endl << " >> Enter information of new distributor";
                        cout << endl << " >> Enter id: ";
                        cin >> id;
                        if(findDistributorById(root, id) != NULL){
                            cout << endl << " >> Id existed, Enter other id"<< endl;
                            break;
                        }
                        cout << " >> Enter name: ";
                        cin >> name;
                        cout << " >> Enter parentId: ";
                        cin >> parentId;
                        Distributor *parentDistributor = findDistributorById(root, parentId);
                        if(parentDistributor == NULL){
                            cout << endl << " >> ParentId doesn't exist, Enter other parentId"<< endl;
                            break;
                        }
                        newDistributor = createDistributor(id, name);
                        newDistributor = insertDistributor(parentDistributor, newDistributor);
                        cout << endl << " >> Your superior distributor has Id = " << newDistributor->parent->id << endl;
                    }
                    addNewDistributorToDatabase("Distributor.csv", newDistributor);
                    cout << endl << " === Created Successfully ===" << endl;
                    break;
                }

                case 2:{
                    int id;
                    int cnt = countDistributor(root);
                    if(cnt == 0){
                        cout << endl << " >> Do not exist any distributor"<< endl;
                        break;
                    }
                    cout << endl << " >> Enter Id of distributor which you want to delete: ";
                    cin >> id;
                    Distributor *delDistributor = findDistributorById(root, id);
                    if(delDistributor == NULL){
                        cout << endl << " >> Don't exist distributor with this Id."<< endl;
                        break;
                    }else{
                        if(delDistributor == root){
                            delDistributor = deleteDistributor(delDistributor);                            
                            root = delDistributor;
                        }else{
                            delDistributor = deleteDistributor(delDistributor);
                        }
                        updateDistributorDatabase(root);
                        cout << endl << endl << " === Deleted Successfully ===" << endl;
                    }
                    break;
                }

                case 3:{
                    int countBatch;
                    ifstream infs;
                    string line;
                    infs.open("Number Of Batch Sale.csv");
                    if(infs.is_open()){
                        getline(infs,line);
                        infs.close();
                    }else{
                        cout << endl << " >> Cannot open file Number Of Batch Sale"<< endl;
                        line = "";
                    }
                    if(line == ""){
                        countBatch = 0;
                    }else{
                        countBatch = stoi(line, nullptr, 10);
                    }

                    countBatch += 1;

                    cout << endl << " >> Enter sales of batch " << countBatch << endl;
                    map<int, Sale*> joinById;
                    while(true){
                        int id, sales;
                        cout << endl << " >> Enter -1 to exit, Enter Id: ";
                        cin >> id;
                        if(id==-1){
                            break;
                        }
                        if(findDistributorById(root, id) == NULL){
                            cout << endl << " >> Don't exist id = " << id << endl;
                            continue;
                        }
                        cout << endl << " >> Enter sales of this Id: ";
                        cin >> sales;
                        Sale *distributorSale = createSale(countBatch, id, sales, 0);
                        joinById[distributorSale->id] = distributorSale;
                    }

                    calculateCommission(root, joinById);

                    ofstream saleFile;
                    saleFile.open("Sales.csv",ios::app|ios::ate);
                    if(saleFile.is_open()){
                        if(countBatch == 1){
                            saleFile << "Batch,Id,Sale,Commission"<< endl;
                        }                        
                        updateSaleDatabase(saleFile, joinById);
                        saleFile.close();
                        cout << endl << " === Enter Successfully ===" << endl;
                    }else{
                        cout << endl << " >> Cannot open file Sales.csv" << endl;
                    }
                    
                    ofstream outfs;
                    outfs.open("Number Of Batch Sale.csv");
                    if(outfs.is_open()){
                        outfs << countBatch;
                        outfs.close();
                    }else{
                        cout << endl << " >> Cannot open file Number Of Batch Sale.csv" << endl;
                    }
                    break;
                }

                default:{
                    cout << endl << " >> Select again from key 1 to 4"<< endl;
                    break;
                }
            }
        }

        char text;
        cout << endl << " >> Continue [any key] or exit program [q||Q]: "<< endl;
        if (text == 'q' || text == 'Q'){
            break;
        }
    }
    return 0;
}
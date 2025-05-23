campus=input()
if(campus=='yes'):
    block=input()
    if(block=='yes'):
        caridar=input()
        if(caridar=='yes'):
            clas=input()
            if(clas=='yes'):
                print('attended the session')
            else:
                print('not atended the session')
        else:
            print('not entered into caridar')
    else:
        print('not enetered into the block')
else:
    print('not entered into the campus')
                

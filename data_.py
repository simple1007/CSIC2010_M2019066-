# -*- encoding: utf-8 -*-
from urllib.parse import unquote
encoding = 'utf-8'

def generate_data(filename,norm=True):
    gen_filename = filename.replace('.txt','_gen.txt')
    
    test_f = open(gen_filename,'w',encoding=encoding)
    with open(filename,encoding=encoding) as f:
        param_count = 0
        f.readline()
        for index,line in enumerate(f):
            if line != '\n':
                # if line.startswith('GET'):
                test_f.write(line)
#                 test_f.write(unquote(line))
                # else:
                #     test_f.write(line)

            else:
                param_count += 1
                if param_count == 2:
                    test_f.write('\n')
                    param_count = 0
                
    test_f.close()

vocab_get = {}
vocab_post = {}
vocab_post['<PAD>'] = 0
vocab_post['<UNK>'] = 1
post_index = 2
get_index = 0
# post_index = 0 
vocab_char = {}
vocab_char['<PAD>'] = 0
char_index = 1
content_type = {}
content_type['UNK'] = 0
content_type_index = 1
accept = {}
accept_index = 0
def vocab_create(filename,test=False):

    global vocab_get,vocab_post,get_index,post_index,vocab_char,char_index,accept,accept_index,content_type,content_type_index

    gen_filename = filename.replace('.txt','_gen.txt')

    gen_file = open(gen_filename,encoding=encoding)

    context = []
    for line in gen_file:
        if line != '\n':
            context.append(line)
        if line.startswith('Accept:'): 
            temp = line.replace('Accept: ','').replace('\n','')
            temp_ = temp.split(',')
            # print(temp)
            for t in temp_:
                # print(t)
                if t not in accept:
                    accept[t] = accept_index
                    accept_index += 1
        elif line.startswith('Content-Type:'):
            temp = line.replace('Content-Type: ','').replace('\n','')
            if temp not in content_type:
                content_type[temp] = content_type_index
                content_type_index += 1
        #문맥(한번의 통신)일경우 bigram 분석    
        else:
            url = context[0]

            if url.startswith('GET'):
                for i in range(len(url)-1):
                    if url[i:i+2] not in vocab_post and not test:
                        vocab_post[url[i:i+2]] = post_index
                        post_index += 1
                for c in list(url):
                    if c not in vocab_char and test:
                        vocab_char[c] = char_index
                        char_index += 1
            else:
                param = context[-1]
                for i in range(len(url)-1):
                    if url[i:i+2] not in vocab_post and not test:
                        vocab_post[url[i:i+2]] = post_index
                        post_index += 1
                for i in range(len(param)-1):
                    if param[i:i+2] not in vocab_post and not test:
                        vocab_post[param[i:i+2]] = post_index
                        post_index += 1
                        # print(param[i:i+2])
                for c in list(url):
                    if c not in vocab_char and not test:
                        vocab_char[c] = char_index
                        char_index += 1
                for c in list(param):
                    if c not in vocab_char and not test:
                        vocab_char[c] = char_index
                        char_index += 1
            if line == '\n':
                context = []

import csv

max_len_url = []
max_len_param = []
def generate_train():
    global max_len_url,max_len_param
    data = open('train.csv','w',encoding=encoding, newline="")
    wr = csv.writer(data)

    norm = open('norm_train_gen.txt',encoding=encoding)
    anorm = open('anomal_train_gen.txt', encoding=encoding)
    count = 0
    context = []
    for line in norm:
        norm_ = 1
        if line != '\n':
            context.append(line)
        #문맥(한번의 통신)일경우 bigram 분석    
        else:
            url = context[0]
            max_len_url.append(len(url))
            if url.startswith('GET'):
                wr.writerow([url.replace('\n',''),'',norm_])
                count+=1
            else:
                param = context[-1]
                max_len_param.append(len(param))
                wr.writerow([url.replace('\n',''),param.replace('\n',''),norm_])
                count+=1
            context = []
        
        #if count == 5013:
        #    break
    context = []

    for line in anorm:
        norm_ = 0
        if line != '\n':
            context.append(line)
        #문맥(한번의 통신)일경우 bigram 분석    
        else:
            url = context[0]
            max_len_url.append(len(url))
            if url.startswith('GET'):
                wr.writerow([url.replace('\n',''),'',norm_])
            else:
                param = context[-1]
                max_len_param.append(len(param))
                wr.writerow([url.replace('\n',''),param.replace('\n',''),norm_])
            
            context = []

def generate_test():
    global max_len_param, max_len_url
    data = open('test.csv','w',encoding=encoding, newline="")
    wr = csv.writer(data)

    norm = open('norm_test_gen.txt',encoding=encoding)
    anorm = open('anomal_test_gen.txt', encoding=encoding)

    context = []
    for line in norm:
        norm_ = 1
        if line != '\n':
            context.append(line)
        #문맥(한번의 통신)일경우 bigram 분석    
        else:
            url = context[0]
            max_len_url.append(len(url))
            if url.startswith('GET'):
                wr.writerow([url.replace('\n',''),'',norm_])
            else:
                param = context[-1]
                max_len_param.append(len(param))
                wr.writerow([url.replace('\n',''),param.replace('\n',''),norm_])
            
            context = []
    
    context = []

    for line in anorm:
        norm_ = 0
        if line != '\n':
            context.append(line)
        #문맥(한번의 통신)일경우 bigram 분석    
        else:
            url = context[0]
            max_len_url.append(len(url))
            if url.startswith('GET'):
                wr.writerow([url.replace('\n',''),'',norm_])
            else:
                param = context[-1]
                max_len_param.append(len(param))
                wr.writerow([url.replace('\n',''),param.replace('\n',''),norm_])
            
            context = []
    
#     wr.close()
    with open('train.csv','r',encoding=encoding) as f:
        re = f.readlines()
    
    import random
    random.shuffle(re)
    
    with open('train.csv','w',encoding=encoding) as f:
        f.writelines(re)

import pickle
if __name__ == '__main__':
    generate_data('norm_train.txt')
    generate_data('norm_test.txt')
    generate_data('anomal_train.txt')
    generate_data('anomal_test.txt')

    vocab_create('norm_train.txt')
    vocab_create('norm_test.txt',test=True)
    vocab_create('anomal_train.txt')
    vocab_create('anomal_test.txt',test=True)
    
    generate_train()
    generate_test()

    print("url: %d" % max(max_len_url))
    print("param: %d" % max(max_len_param))
    with open('vocab_get.pkl','wb') as f:
        pickle.dump(vocab_get,f)
    with open('vocab_post.pkl','wb') as f:
        pickle.dump(vocab_post,f)
    with open('accept.pkl','wb') as f:
        pickle.dump(accept,f)
    with open('content_type.pkl','wb') as f:
        pickle.dump(content_type,f)
    with open('vocab_char.pkl','wb') as f:
        pickle.dump(vocab_char,f)
    # a = 'http://localhost:8080/tienda1/publico/anadir.jsp?id=3&nombre=Vino+Rioja&precio=39%3C%21--%23include+file%3D%22archivo_secreto%22+--%3E&cantidad=3&B1=A%F1adir+al+carrito HTTP/1.1'
    # print(unquote(a))

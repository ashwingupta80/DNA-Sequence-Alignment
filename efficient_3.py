import time
import sys
import psutil

delta_e=30
mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
alpha = [[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]]


def string_generate(filepath,str_slt1,str_slt2, ls_1, ls_2):
    bstr1, bstr2="",""
    with open(filepath, 'r') as inpFile: 
        rl = inpFile.read().splitlines()
        for l in rl:
            if str_slt1==False and l.isdigit()!=True:
                str_slt1,bstr1=True, l
            elif l.isdigit()!=True:
                str_slt2,bstr2=True,l
            if str_slt2==False and l.isdigit():
                l=int(l)
                ls_1.append(l)
            elif l.isdigit():
                l=int(l)
                ls_2.append(l)
    h=0
    while h<len(ls_2):
        bv=ls_2[h]+1
        snd_half= bstr2 + bstr2[bv:]
        bstr2=bstr2[:bv] + snd_half
        h+=1
    h=0
    while h<len(ls_1):
        bv2=ls_1[h]+1
        snd_half2=bstr1 + bstr1[bv2:]
        bstr1=bstr1[:bv2] + snd_half2
        h+=1
    return bstr1,bstr2

def sequence_alignment(string1, string2,m,n,dp_row,dp_col):
    
    cost_mat = [([0]*dp_col) for i in range(dp_row)]
    if dp_col-1==0:
        z2="_" * (dp_row-1)
        return  string1 , z2,(dp_row-1)*delta_e
    if dp_row-1==0:
        z1="_" * (dp_col-1 )
        return z1 , string2,(dp_col-1)*delta_e 
    rw_1=1
    while rw_1<dp_row:
        cost_mat[rw_1][0] = rw_1*delta_e
        rw_1=rw_1+1
    
    rw_2=1
    while rw_2<dp_col:
        cost_mat[0][rw_2] = rw_2*delta_e
        rw_2=rw_2+1  

    for q in range(1 , dp_row):
        for r in range(1 , dp_col):
            if string2[r - 1]==string1[q - 1]:
                # If string matches at indices then take the diagonal element.
                cost_mat[q][r] = cost_mat[q - 1][r - 1]
            else:
                # Else take the minimum of row, col( with deltas), or diagonal with mismatch cost.
                cost_mat[q][r] = min(cost_mat[q - 1][r] + delta_e , cost_mat[q - 1][r - 1] + alpha[mapping[string1[q - 1]]][mapping[string2[r - 1]]]
                            ,cost_mat[q][r - 1] + delta_e)
    
    
    q,r = dp_row-1, dp_col-1
    X_seq,Y_seq="",""
    while (r!=0 and q!=0):
        if string2[r - 1] ==string1[q - 1] or cost_mat[q][r] == cost_mat[q - 1][r - 1] + alpha[mapping[string1[q - 1]]][mapping[string2[r - 1]]] :
            X_seq += string1[q - 1]
            Y_seq += string2[r - 1]
            r,q = r - 1, q - 1
        elif  delta_e + cost_mat[q][r - 1]  == cost_mat[q][r]:
            Y_seq += string2[r - 1]
            r -= 1
            X_seq += "_"    
        elif delta_e + cost_mat[q - 1][r]  == cost_mat[q][r]:
            Y_seq += "_"
            X_seq += string1[q - 1]
            q -= 1
    while r>0:
        Y_seq += string2[r - 1]
        r -= 1
        X_seq += "_"
    while q>0:
        X_seq += string1[q - 1]
        q -= 1
        Y_seq = '_' + Y_seq
    return  X_seq[::-1],Y_seq[::-1],cost_mat[m][n]


def Space_eff(X, Y):
    gg=len(X)+1
    gg2=len(Y)+1
    str1,output = [0]*gg,[]
    str2 = [0]*gg
    for _ in range(gg):
        str1[_] = delta_e*_
    i1=1
    output.append(str1[-1])
    while i1<gg2:
        str2[0] = delta_e*i1
        for i2 in range(1, gg):
            str2[i2] = min(delta_e + str2[i2-1],alpha[mapping[Y[i1-1]]][mapping[X[i2-1]]] + str1[i2-1], str1[i2]+delta_e)
        output.append(str2[-1])
        i1+=1
        str1 = str2[:]
    return output

def Divide_and_Conquer(X, Y):
    index_m = -1
    n, m = len(Y), len(X)
    dp_row, dp_col = m+1,n+1
    if dp_row<=3 or dp_col<=3:
        return sequence_alignment(X,Y,m,n,dp_row,dp_col)
    mdtr = ((dp_row-1)//2)
    xstr_r = X[mdtr:]
    sg=0
    xstr_l = X[:mdtr]
    rght_seg = Space_eff(xstr_r[::-1], Y[::-1])[::-1]
    num_m=float("inf")
    lft_seg = Space_eff(xstr_l, Y) 
    
    while sg<len(lft_seg):
        if rght_seg[sg]+lft_seg[sg]<=num_m:
            num_m ,index_m= rght_seg[sg]+lft_seg[sg],sg
        sg+=1
    x2str_r = Y[index_m:]   
    x2str_l = Y[0:index_m]
    cost2, X_r,Y_r = Divide_and_Conquer(xstr_r, x2str_r)
    cost1,X_l,Y_l = Divide_and_Conquer(xstr_l, x2str_l)
    
    return cost1 + cost2,X_l+X_r, Y_l+Y_r   

def main():
    str_slt1=False
    str_slt2=False
    ls_1,ls_2=[],[]
    inpFile = sys.argv[1]
    string1, string2 = string_generate(inpFile,str_slt1,str_slt2,ls_1,ls_2)
    srt_tm = time.time()
    X_seq, Y_seq, total_cost = Divide_and_Conquer(string1,string2)
    total_time = (time.time() - srt_tm)*1000
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)  
    outputfile = open(sys.argv[2], "w+")
    out1 = [ str(total_cost) + "\n",X_seq+ "\n",  Y_seq + "\n", str(total_time) + "\n", str(memory_consumed) + "\n"]
    outputfile.writelines(out1)
    outputfile.close()

if __name__ == "__main__":
    main()

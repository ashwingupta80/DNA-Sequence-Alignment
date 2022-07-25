import time
import psutil
import sys


def string_generate(inpFile,str_slt1,str_slt2, ls_1, ls_2):
    bstr1, bstr2="",""
    with open(inpFile, 'r') as inpf: 
        rl = inpf.read().splitlines()
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
delta_e=30
mapping={"A":0,"C":1,"G":2,"T":3}
alpha = [[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]
def sequence_alignment(X,Y,m,n,dp_row, dp_col):
    cost_mat = [([0]*dp_col) for _ in range(dp_row)]
    # If either one of the string is empty return gaps of the length of the other one.
    if dp_col-1==0:
        z2="_" * (dp_row-1)
        return (dp_row-1)*delta_e, X , z2
    if dp_row-1==0:
        z1="_" * (dp_col-1 )
        return (dp_col-1)*delta_e, z1 , Y 
    # Initialise dependendent rows and columns value in cost matrix for dynamic programming.
    rw_1=1
    while rw_1<dp_row:
        cost_mat[rw_1][0] = delta_e*rw_1
        rw_1=rw_1+1
    
    rw_2=1
    while rw_2<dp_col:
        cost_mat[0][rw_2] = delta_e*rw_2
        rw_2=rw_2+1    
    
    # Top down pass
    for q in range(1 , dp_row):
        for r in range(1 , dp_col):
            if Y[r - 1]==X[q - 1]:
                # If string matches at indices then take the diagonal element.
                cost_mat[q][r] = cost_mat[q - 1][r - 1]
            else:
                # Else take the minimum of row, col( with deltas), or diagonal with mismatch cost.
                cost_mat[q][r] = min(cost_mat[q - 1][r] + delta_e , cost_mat[q - 1][r - 1] + alpha[mapping[X[q - 1]]][mapping[Y[r - 1]]]
                            ,cost_mat[q][r - 1] + delta_e)
    
    q,r = dp_row-1, dp_col-1
    X_seq,Y_seq="",""
    
    # bottom up pass
    while (r!=0 and q!=0):
        if Y[r - 1] ==X[q - 1] or cost_mat[q][r]==cost_mat[q - 1][r - 1] + alpha[mapping[X[q - 1]]][mapping[Y[r - 1]]]:
            X_seq += X[q - 1]
            Y_seq += Y[r - 1]
            r,q = r - 1, q - 1
        elif (delta_e + cost_mat[q][r - 1])== cost_mat[q][r]:
            Y_seq += Y[r - 1]
            r -= 1
            X_seq += "_"
        elif (delta_e + cost_mat[q - 1][r]) == cost_mat[q][r]:
            Y_seq += "_"
            X_seq += X[q - 1]
            q -= 1
    while r>0:
        Y_seq += Y[r - 1]
        r -= 1
        X_seq += "_"
    while q>0:
        X_seq += X[q - 1]
        q -= 1
        Y_seq = '_' + Y_seq
    return cost_mat[m][n],X_seq[::-1], Y_seq[::-1] 



def main():
    str_slt1=False
    str_slt2=False
    ls_1,ls_2=[],[]
    inpFile = sys.argv[1]
    str1, str2 = string_generate(inpFile,str_slt1,str_slt2,ls_1,ls_2)
    dp_row=len(str1)+1
    dp_col=len(str2)+1
    srt_tm = time.time()
    cost,x_seq, y_seq = sequence_alignment(str1,str2, len(str1), len(str2),dp_row, dp_col)
    total_time = (time.time() - srt_tm)*1000
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)     
    outputfile = open(sys.argv[2], "w+")
    out1 = [ str(cost) + "\n",x_seq+ "\n",  y_seq + "\n", str(total_time) + "\n", str(memory_consumed) + "\n"]
    outputfile.writelines(out1)
    outputfile.close()


if __name__ == "__main__":
    main()

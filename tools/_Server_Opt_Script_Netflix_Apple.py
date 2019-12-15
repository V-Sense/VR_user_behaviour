# =============================================================================
#  Script to evaluate server optimisation for VR tile-based ODV presented in
# "Do Users Behave Similarly in VR? Investigation of the User Influence on the System Design"
# Author: Silvia Rossi  (s.rossi@ucl.ac.uk)
#         Cagri Ozcinar (ozcinarc@ scss.tcd.ie,)
#         Aljosa Smolic (smolica@scss.tcd.ie)
#         Laura Toni    (l.toni@ucl.ac.uk)
# =============================================================================

import pulp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from collections import defaultdict
import sys
import csv
import os

def main():
    
         # =============================================================================
    #                              ###----------------------###
    #                              ###   Support function   ###
    #                              ###----------------------###
    # =============================================================================
        
    def c_e(mu_e,resolution):
         if resolution <= 720:
             c_1 = mu_e
         elif resolution <= 1080:
             c_1 = 2*mu_e
         elif resolution <= 4000:
             c_1 = 4*mu_e
         else:
             c_1 = 8*mu_e
    
         return c_1
    
    #def c_s(mu_s,BitValue):
    #    cost_tot =  BitValue*mu_s
    #    return cost_tot
    
    def find_res_heatmap(dev_name):
        res_heatmap = np.zeros(2)
        res_heatmap[0]= d_res[dev_name][0]
        res_heatmap[1] = d_res[dev_name][1]
        return res_heatmap
    
    def find_res_tiles(dev,N):
        res_tiles = np.zeros((N,2))
        for i_t in range(0,N):
            if i_t == 0 or i_t == N-1:
                res_tiles[i_t] = d_res[dev][0]
                res_tiles[i_t,1] = d_res[dev][1]/4
            else:
                res_tiles[i_t] = d_res[dev][0]/4
                res_tiles[i_t,1] = d_res[dev][1]/2
        return res_tiles
    
    def read_RD(videoName, Rates, ch, name_base):
        q = np.zeros((Users_num,N,len(Rates),len(sp_index)))
        #q[:,:,0]=100
        for u in range(Users_num):
        
            d_name = Users_cat.Device[u]
            
            res_h= find_res_heatmap(d_name)
            
            ### read csv file of distortion
            ##print('RD_' + str(int(res_h[0])) + 'x' + str(int(res_h[1])) + name_base +'.csv')
            table = pd.read_csv('RD_' + str(int(res_h[0])) + 'x' + str(int(res_h[1])) + name_base +'.csv')
    
            for s in range(len(sp_index)):
                select_index = sorted(list(set(table.index[table.sequence == videoName].tolist()) & set(table.index[table.chunk == ch].tolist()) & set(table.index[table.res_scheme == sp_name_table[int(s)]].tolist())))
                for j in range(N):
                    for r in range(len(Rates)):
                        ##print(str([u]) + str([j]) + str([r]) + str([s]))
                        q[u][j][r][s]=table.at[select_index[r],'d_'+str(j)]
        return q
    
    def read_RD_B(videoName, ch):
        q = np.zeros((Users_num,N,len(Rates),len(sp_index)))
        q[:,:,0]= 100000
        for u in range(Users_num):
        
            d_name = Users_cat.Device[u]
            
            res_h= find_res_heatmap(d_name)
            
            ### read csv file of distortion
            #print('RD_' + str(int(res_h[0])) + 'x' + str(int(res_h[1])) + '.csv')
            table = pd.read_csv('RD_' + str(int(res_h[0])) + 'x' + str(int(res_h[1])) + '.csv')
    
            for s in range(0,len(sp_index)):
                select_index = sorted(list(set(table.index[table.sequence == videoName].tolist()) & set(table.index[table.chunk == ch].tolist()) & set(table.index[table.res_scheme == sp_name_table[int(s)]].tolist())))
                for j in range(0,N):
                    for r in range(0,len(BitRate)-1):
                        q[u][j][r+1][s]=table.at[select_index[r],'d_'+str(j)]
        return q
    
    def tiles_prob(videoName, ch):
        
        prob = np.zeros((Users_num,N))
        
        for u in range(Users_num):

            d_name = Users_cat.Device[u]
            d_idx = Devices.index(d_name)
            
            #print('::File: ' + 'dev_' + str(d_idx) + '/' + videoName + '_dev_' + str(d_idx) + '_sec_' + str(ch*length_ch) + '.npy')
            ### read csv file of distortion
            # print( 'dev_' + str(S) + '.csv')
            if index_probDev == str(5) or index_probDev == str(6):
                table = pd.read_csv('prob_dev_0.csv', names = ['folder','file','p_0','p_1','p_2','p_3','p_4','p_5'])
                table = table[table.file == videoName + '_dev_0_sec_' + str(ch*length_ch) + '.npy']        
            # prob[int(S)][j]
    
                prob[int(u)] = [table['p_' + str(j)].values[0] for j in range(0,N)]
                
                table = pd.read_csv('prob_dev_1.csv', names = ['folder','file','p_0','p_1','p_2','p_3','p_4','p_5'])
                table = table[table.file == videoName + '_dev_1_sec_' + str(ch*length_ch) + '.npy']        
            # prob[int(S)][j]
    
                prob[int(u)] = prob[int(u)]*[table['p_' + str(j)].values[0] for j in range(0,N)]
                
                table = pd.read_csv('prob_dev_2.csv', names = ['folder','file','p_0','p_1','p_2','p_3','p_4','p_5'])
                table = table[table.file == videoName + '_dev_2_sec_' + str(ch*length_ch) + '.npy']        
            # prob[int(S)][j]
    
                prob[int(u)] = prob[int(u)]*[table['p_' + str(j)].values[0] for j in range(0,N)]
                prob[int(u)] = prob[int(u)]/3
                prob[int(u)] = prob[int(u)]/sum(prob[int(u)])
                
            else:
                table = pd.read_csv('prob_dev_' + str(d_idx) + '.csv', names = ['folder','file','p_0','p_1','p_2','p_3','p_4','p_5'])
                table = table[table.file == videoName + '_dev_' + str(d_idx) + '_sec_' + str(ch*length_ch) + '.npy']        
            # prob[int(S)][j]
    
                prob[int(u)] = [table['p_' + str(j)].values[0] for j in range(0,N)]

        return prob
    
    def print_Results_opt(scenario_name, BitRate, Rates):
        print('SCENARIO ' + scenario_name + ' PRINT RESULTS ')
        # The status of the solution is printed to the screen
        print("Status: ", pulp.LpStatus[model.status])
        print('Chunk = ' + str(ch))

        check_quality = 0
        check_encoding_c = 0
        check_stor_c = 0

        for u in Users:
        
            dev = Users_cat.Device[int(u)]
            
            if ch == 0:
                with open(scenario + '_Scenario.txt', 'a+') as alphaFile:
                    alphaFile.write(videoName + ' ' + u + ' ' + str(Users_cat.Prob_u[int(u)]) + ' ' + str(Users_cat.Device[int(u)]) + ' ' + str(Users_cat.Prob_d[int(u)]) + ' ' + str(Users_cat.Network[int(u)]) + ' ' + str(Users_cat.Prob_n[int(u)]) + ' ' + str(Users_cat.BW_u[int(u)]) + ' ' + str(Users_cat.Prob_BW[int(u)]) +  ' ' + str(mu_e) + ' ' + str(mu_s) + ' ' + str(lambda_cost) + ' ' + str(CostMax) + '\n')
                alphaFile.close()
            
            
            check_rates = 0

            print('Dev: ' + dev + ' With network: ' + Users_cat.Network[int(u)] + ' BW = ' + str(Users_cat.BW_u[int(u)]))
            print('Prob User type = ' + str(Users_cat.Prob_u[int(u)]))
                    
            for j in Tiles:
                for r in Rates:
                    for s in sp_index:
            #print('Tiles ' + j + ' -> ' + str(d[int(j)][int(r)]*prob[int(j)]))
                        if pulp.value(alpha[u][j][r][s])>=1:
                           # print( ' - Tiles ' + j + ' is select at quality level = ' + r + ' (' + str(BitRate[int(r)]) + 'kbps) with Distortion = ' + str(q[int(u)][int(j)][int(r)]) + ' sp = ' + s)
                            
                            check_quality += q[int(u)][int(j)][int(r)][int(s)]*S_tiles[int(j)]*prob[int(u)][int(j)]*Users_cat.Prob_u[int(u)]
                            check_rates += BitRate[int(r)]
                            
                            with open(scenario + '_OptResults_alpha.txt', 'a+') as alphaFile:
                                alphaFile.write(videoName + ' ' + str(ch) + ' ' + j + ' ' + r +  ' '   + s + ' ' +  u + ' ' + str(prob[int(u)][int(j)]) + ' ' +  str(q[int(u)][int(j)][int(r)][int(s)]) + ' ' + str(Rates[int(r)]) + ' ' + str(sp_tiles_w[sp_name_table[int(s)]][int(j)]) + ' ' + str(sp_tiles_h[sp_name_table[int(s)]][int(j)]) + '\n')
                            alphaFile.close()

            print(str(check_rates) + ' - BW = ' + str(Users_cat.BW_u[int(u)]))               
            
            if check_rates > Users_cat.BW_u[int(u)]:
                print('ERROR BW')
        
        print('quality val = ' + str(check_quality) )
        print('Obj function value = ' + str(pulp.value(model.objective)))
        
        #print('Check BETA and save data')
        if len(BitRate)> 10:
            flag = 1
        else:
            flag = 0

        d_1 = np.where(Users_cat['Device'] == 'HMD')
        d_2 = np.where(Users_cat['Device'] == 'Laptop')
        d_3 = np.where(Users_cat['Device'] == 'Tablet')
        #Save data - csv
        for j in Tiles:
            for s in sp_index:
                for r in Rates:
                    if flag == 1 and int(r) > 0 and pulp.value(beta[j][r][s])==1:
                        
                        #print('Save Beta in flag = ' + str(flag))
                            
                        check_stor_c  += mu_s*BitRate[int(r)]
                        check_encoding_c += c_e(mu_e*length_ch, sp[int(s)][1])/N
                        
                       # print('Tiles ' + j + ' is stored at quality level = ' + r + ' (' + str(BitRate[int(r)]) + 'kbps) with Distortion = ' + str(q[int(u)][int(j)][int(r)][int(s)]) + ' with sp = ' + s)
                        with open(scenario + '_OptResults.csv', 'a') as csvFile:
                            writer = csv.writer(csvFile)
                            writer.writerow([videoName, str(ch), j, str(Rates[int(r)]), s, str(sp_tiles_w[sp_name_table[int(s)]][int(j)]) + 'x' + str(sp_tiles_h[sp_name_table[int(s)]][int(j)])])
                        csvFile.close()
                        with open(scenario + '_OptResults_beta.txt', 'a+') as BetaFile:
                            BetaFile.write(videoName + ' ' + str(ch) + ' ' + j + ' ' + r +  ' '   + s +  ' ' + str(Rates[int(r)]) + ' ' + str(sp_tiles_w[sp_name_table[int(s)]][int(j)]) + ' ' + str(sp_tiles_h[sp_name_table[int(s)]][int(j)]) + ' ' + str(q[int(d_1[0][0])][int(j)][int(r)][int(s)]) + ' ' + str(q[int(d_2[0][0])][int(j)][int(r)][int(s)]) + ' ' + str(q[int(d_3[0][0])][int(j)][int(r)][int(s)]) + '\n')
                        BetaFile.close()
                    elif flag == 0 and pulp.value(beta[j][r][s])==1:
                        
                        #print('Save Beta in flag = ' + str(flag))
                    
                        check_stor_c  += mu_s*BitRate[int(r)]
                        check_encoding_c += c_e(mu_e*length_ch, sp[int(s)][1])/N
                        
                        # print('Tiles ' + j + ' is stored at quality level = ' + r + ' (' + str(BitRate[int(r)]) + 'kbps) with Distortion = ' + str(q[int(u)][int(j)][int(r)]) + ' with sp = ' + s)
                        with open(scenario + '_OptResults.csv', 'a') as csvFile:
                            writer = csv.writer(csvFile)
                            writer.writerow([videoName, str(ch), j, str(Rates[int(r)]), s, str(sp_tiles_w[sp_name_table[int(s)]][int(j)]) + 'x' + str(sp_tiles_h[sp_name_table[int(s)]][int(j)])])
                        csvFile.close()
                        with open(scenario + '_OptResults_beta.txt', 'a+') as BetaFile:
                            BetaFile.write(videoName + ' ' + str(ch) + ' ' + j + ' ' + r +  ' '   + s +  ' ' + str(BitRate[int(r)]) + ' ' + str(sp_tiles_w[sp_name_table[int(s)]][int(j)]) + ' ' + str(sp_tiles_h[sp_name_table[int(s)]][int(j)]) + ' ' + str(q[int(d_1[0][0])][int(j)][int(r)][int(s)]) + ' ' + str(q[int(d_2[0][0])][int(j)][int(r)][int(s)]) + ' ' + str(q[int(d_3[0][0])][int(j)][int(r)][int(s)]) + '\n')
                        BetaFile.close()
                        

        
        with open(scenario + '_OptResults_objValues.txt', 'a+') as ObjFile:
            ObjFile.write(videoName + ' ' + str(ch) + ' ' + str(pulp.value(model.objective)) + ' ' + str(check_quality) + ' ' + str(check_encoding_c) + ' ' +  str(check_stor_c) + ' ' + '\n')
        ObjFile.close()       
        
        print('cost server stor cost = ' + str(check_stor_c*lambda_cost))
        print('cost server encoding cost = ' + str(check_encoding_c*lambda_cost))
        print('Video ' + videoName_all[0])
        print('SCENARIO ' + scenario_name + ' Name simulation = ' + name_file + 'lambda = ' + str(lambda_cost))
        print('prob_devs: \n' + str(prob_Devices))
        print('prob_Netwoks per Devices: \n' + str(prob_Networks))
        print('BW_type: \n' + str(BW_type))
        
        return
    
    
    
    print("Start sim. ")
    
    name_file = input('Name simulations for scenario (i.e., data)? ')
   
    # =============================================================================
    #                              ###---------------------------------###
    #                              ###   Set problem data commun data  ###
    #                              ###---------------------------------###
    # =============================================================================
    
     #### n tiles with index j ---- for now i will consider a regular grid for tiles I need to ask the size to cagri of poles' tiles
    N = 6
    
    ### coding rate r = R
    BitRate_Netflix = [391.67, 500, 716.67, 966.67, 1300, 1916.67]#kbps
    Res_Netflix = ['2','2','1','1','0','0']

    BitRate_Apple = [400, 483.33, 566.67, 641.67, 900, 966.67, 1166.67, 1350, 1616.67]#kbps
    Res_Apple = ['2','2','2','2','1','1','1','1','0','0']
    
    #DEVICE resolution
    d_res = pd.DataFrame({'HMD':[3840, 2160], 'Laptop':[1920, 1080], 'Tablet':[2560, 1440]})
    
    ### VIDEO Resolution
    sp = [[2560, 1440], [1920, 1080],[1280, 720]]#, [960, 540]]        #resolutions RD
    #sp_tiles = pd.DataFrame({'sp1_tiles_0_N':[2560, 360], 'sp1_tiles': [640, 720], 'sp2_tiles_0_N': [1920, 270], 'sp2_tiles': [480, 540], 'sp3_tiles_0_N':[1280, 180], 'sp3_tiles':[320, 540],'sp4_tiles_0_N':[854, 120], 'sp4_tiles': [213, 240]})
    sp_tiles_w = pd.DataFrame({'sp1': [2560, 640, 640, 640, 640,2560], 'sp2': [1920, 480, 480, 480, 480, 1920], 'sp3': [1280, 320, 320, 320, 320, 1280]})#, 'sp4': [960, 240, 240, 240, 240, 960]})
    sp_tiles_h = pd.DataFrame({'sp1': [360, 720,720,720,720, 360], 'sp2':[270, 540, 540, 540, 540, 270], 'sp3':[180, 360, 360, 360, 360,180]})#, 'sp4': [135, 270, 270, 270, 270, 135] })
    sp_name_table = ['sp1', 'sp2', 'sp3']#, 'sp4']
    sp_index = ['0','1','2']
    Devices = ['HMD','Tablet', 'Laptop']
    # when I will have all the resolution i need to extend this matrix to all case
    #device_tiles = pd.DataFrame({'HMD - W':[3840, 960, 960, 960, 960, 3840], 'HMD - H':[540, 1080, 1080, 1080, 1080, 540]})
    
    S_tiles = [0.032, 0.234,  0.234,  0.234,  0.234, 0.032]
    
    ##Other parameters - fixed for now
    #videoName_all = ['v01_BabyPandas', 'v02_FighterJet', 'v03_HollywoodRockit','v06_Back2theMoon', 'v07_HELP', 'v09_Symphony','v11_GetBarreled','v13_KITZ','v15_OceanShark','v18_Dancing', 'v19_Nick', 'v20_Survivorman2', 'v23_Knockout', 'v24_invasion','v25_invisibleMan']
    index_video = input('Which video ? \n 0) v03_HollywoodRockit \n 1) v01_BabyPandas \n 2) v06_Back2theMoon \n 3) v15_OceanShark \n 4) v07_HELP \n 5) v11_GetBarreled 6) v02_FighterJet \n 7) v09_Symphony \n 8) v13_KITZ \n 9) v18_Dancing \n 10) v19_Nick \n 11) v20_Survivorman2 \n 12) v23_Knockout \n 13) v24_invasion \n 14) v25_invisibleMan \n')
    
    if index_video == str(0):
        videoName_all = ['v03_HollywoodRockit']
    elif index_video == str(1):
        videoName_all = ['v01_BabyPandas']
    elif index_video == str(2):
        videoName_all = ['v06_Back2theMoon']
    elif index_video == str(3):
        videoName_all = ['v15_OceanShark']
    elif index_video == str(4):
        videoName_all = ['v07_HELP']
    elif index_video == str(5):
        videoName_all = ['v11_GetBarreled']
    elif index_video == str(6):
        videoName_all = ['v02_FighterJet']
    elif index_video == str(7):
        videoName_all = ['v09_Symphony']
    elif index_video == str(8):
        videoName_all = ['v13_KITZ']
    elif index_video == str(9):
        videoName_all = ['v18_Dancing']
    elif index_video == str(10):
        videoName_all = ['v19_Nick']
    elif index_video == str(11):
        videoName_all = ['v20_Survivorman2']
    elif index_video == str(12):
        videoName_all = ['v23_Knockout']
    elif index_video == str(13):
        videoName_all = ['v24_invasion']
    elif index_video == str(14):
        videoName_all = ['v25_invisibleMan']

    

    Networks_name = ['WiFi','4G','ADSL']
    
    #Networks BW values
    Networks = pd.DataFrame({'WiFi':[3, 30],
                             '4G':  [5, 20],
                             'ADSL':[8, 35]}) #Mbps
    Networks = Networks*1000   #to have kbps
    
    
    prob_Networks = pd.DataFrame({'WiFi':[0.8, 0.45, 0.4],
                                 '4G':  [0, 0, 0.6],
                                 'ADSL':[0.2, 0.55, 0]})
    prob_Networks.index = Devices
    
    index_probDev = input('Which prob. of devices do you want to simulate? \n 0) Only HMD \n 1) Only Laptop \n 2) Only Tablet \n 3) Eq. prob \n 4) p(HMD) highest  \n 5) avg heatmap - eqDev  \n 6) avg heatmap highest HMD \n')

    if index_probDev == str(0):
        prob_Devices = pd.DataFrame({'HMD':[1], 'Laptop':[0], 'Tablet':[0]})
        name_prob = '_onlyHMD'
    elif index_probDev == str(1):
            prob_Devices = pd.DataFrame({'HMD':[0], 'Laptop':[1], 'Tablet':[0]})
            name_prob = '_onlyLaptop'
    elif index_probDev == str(2):
            prob_Devices = pd.DataFrame({'HMD':[0], 'Laptop':[0], 'Tablet':[1]})
            name_prob = '_onlyTablet'
    elif index_probDev == str(3):
        prob_Devices = pd.DataFrame({'HMD':[0.4], 'Laptop':[0.3], 'Tablet':[0.3]})
        name_prob = '_eqDev'
    
    
    BW_type = pd.DataFrame({'Prob': [0.25, 0.5, 0.25],#, 0.5, 0.25],
                            'Perc':[25, 50, 75]})#, 50, 75]})
    
    
    print('prob_devs: \n' + str(prob_Devices))
    print('prob_Netwoks per Devices: \n' + str(prob_Networks))
    print('BW_type: \n' + str(BW_type))
    
    #Build USERS categories
    Users_cat = pd.DataFrame({'Device': [],'Network':[], 'Prob_u': [], 'Prob_n': [], 'Prob_d': [], 'Prob_BW': [], 'BW_u': []})
    
    for d in Devices:
        for n in Networks_name:
            for t in range(len(BW_type.Prob)):
                Users_cat = Users_cat.append({'Device': d,'Network':n, 'Prob_u': prob_Networks.at[d,n]*prob_Devices.at[0,d]*BW_type.Prob[t], 'Prob_n': prob_Networks.at[d,n], 'Prob_d': prob_Devices.at[0,d], 'Prob_BW': BW_type.Prob[t], 'BW_u': np.percentile(Networks[n],BW_type.Perc[t])}, ignore_index=True)
    
    Users_num = Users_cat.index.values[-1] + 1 #num categories of users
    
    Users = []
    for u in range(Users_num):
        Users.append(str(u))
            
    
    ###some for chunk - i will start only with chunk 0
    n_ch = 10
    length_ch = 2 #sec
    
    Rates_Netflix = []
    for r in range(len(BitRate_Netflix)):
        Rates_Netflix.append(str(r))
    
    Rates_Apple = []
    for r in range(len(BitRate_Apple)):
        Rates_Apple.append(str(r))
    
    Tiles = ["0", "1", "2", "3", "4", "5"]
    
    #Cost parameter
    mu_e = 3.12*10**(-3) # $/sec
    mu_s = 2.4*10**(-6) # $/kbps
    lambda_cost = 0;
    CostMax = 0;
    directory = name_file + '_' + videoName_all[0] + '_' + name_prob
                    ###-------------------------------------------------###
                    ###            Create saving file   (D)             ###
                    ###-------------------------------------------------###

    ### Optimization based only on BW constraints - no user interactivity
    
    print(name_file + '_' + videoName_all[0] + '_Netflix_baseline')
    scenario =  directory + '/' + videoName_all[0] + '_Netflix_real'
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    ##To write results
    csvData = ['VideoName', 'ch #','Tiles #', 'Rate Val.', 'sp #', 'Tile Res']

    with open(scenario + '_OptResults.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvData)
    csvFile.close()

    with open(scenario + '_Scenario.txt', 'w') as alphaFile:
        alphaFile.write('#VideoName u p(u) Dev p(d) Network p(n) BW p(BW) mu_e mu_s lambda_cost CostMax\n')
    alphaFile.close()

    with open(scenario + '_OptResults_alpha.txt', 'w') as alphaFile:
        alphaFile.write('#VideoName idx_ch idx_Tiles Quality idx_sp u p(j) Distortion RateVal TileRes(W) TileRes(H) \n')
    alphaFile.close()

    with open(scenario + '_OptResults_beta.txt', 'w') as betaFile:
        betaFile.write('#VideoName idx_ch idx_Tiles Quality idx_sp RateVal TileRes(W) TileRes(H) Distortion(Dev_1) Distortion(Dev_2) Distortion(Dev_3)\n')
    alphaFile.close()

    with open(scenario + '_OptResults_objValues.txt', 'w') as ObjFile:
        ObjFile.write('#VideoName idx_ch objVal(TOT) objVal1 objVal2(enc) objVal3(stor) \n')
    ObjFile.close()

                    ###-------------------------------------------------###
                    ###               Solve SCENARIO (D) baseline                ###
                    ###-------------------------------------------------###


    for videoName in videoName_all:
        for ch in range(n_ch):
            print('Folder : ' + directory)
            print('Chunk = ' + str(ch))
            # The prob variable is created to contain the problem data
            model = pulp.LpProblem("Server Optimization",pulp.LpMinimize)
            
            
            # Decision variables: (they need string as input variable)
            alpha = pulp.LpVariable.dicts("Alpha_DecVar",(Users,Tiles,Rates_Netflix,sp_index),0,1,pulp.LpInteger)
            beta = pulp.LpVariable.dicts('Beta_DecVar',(Tiles,Rates_Netflix,sp_index),0,1,pulp.LpInteger)
            gamma = pulp.LpVariable.dicts('Gamma_DecVar',(Users,sp_index),0,1,pulp.LpInteger)
            
            #tile prob from heatmap for the chunk
            prob = tiles_prob(videoName, ch)
            
            q = read_RD(videoName, Rates_Netflix, ch, '_Netflix')
          
            model += pulp.lpSum([q[int(u)][int(j)][int(r)][int(Res_Netflix[int(r)])]*alpha[u][j][r][Res_Netflix[int(r)]]*S_tiles[int(j)]*Users_cat.Prob_u[int(u)] for u in Users for j in Tiles for r in Rates_Netflix]),"Obj fun"
           
            ### ---- constraints ----
            ### --- a) set up decision variable alpha
            # A constraint ensuring that only one value can be in each square is created
            for u in Users:
                for j in Tiles:
                    model += pulp.lpSum([alpha[u][j][r][s] for r in Rates_Netflix for s in sp_index]) == 1, ""
            print("Constraint A - done")
            
            for s in sp_index:
                for j in Tiles:
                    model += pulp.lpSum([beta[j][r][s] for r in Rates_Netflix]) == 1, ""
                    
            for u in Users:
                model += pulp.lpSum([gamma[u][s] for s in sp_index]) <= 1, ""
            
    #       ### --- b) set up decision variable alpha  and beta
            for u in Users:
                for s in sp_index:
                    for j in Tiles:
                        for r in Rates_Netflix:
                            model += alpha[u][j][r][s] <= beta[j][r][s], ''
                            model += alpha[u][j][r][s] <= gamma[u][s] , ''
            print("Constraint B - done")

            for s in sp_index:
                for j in Tiles:
                    for r in Rates_Netflix:
                        model += beta[j][r][s] <= pulp.lpSum([alpha[u][j][r][s] for u in Users]),""
            ### --- c) set up decision variable beta & alpha
            print("Constraint C - done")

            for u in Users:
                for s in sp_index:
                    model += gamma[u][s] <= pulp.lpSum([alpha[u][j][r][s] for j in Tiles for r in Rates_Netflix]),""

                     ### --- d) set up bw constraints
            for u in Users:
                model += pulp.lpSum([alpha[u][j][r][s]*BitRate_Netflix[int(r)] for r in Rates_Netflix for j in Tiles for s in sp_index]) <= Users_cat.BW_u[int(u)], ""
            print("Constraint D - done")
            
            for u in Users:
                for j in Tiles:
                    for r in Rates_Netflix:
                        for s in sp_index:
                            if int(s) == int(Res_Netflix[int(r)]):
                                model += alpha[u][j][r][s] <= 1 , ''
                            else:
                                model += alpha[u][j][r][s] == 0 , ''

            for u in Users:
                for j in Tiles:
                    for s in sp_index:
                        if Devices[int(s)] == Users_cat.Device[int(u)]:
                            model += pulp.lpSum([alpha[u][j][r][s] for r in Rates_Netflix]) == 1
                        else:
                            model += pulp.lpSum([alpha[u][j][r][s] for r in Rates_Netflix]) == 0
            model.solve()

            print_Results_opt('Netflix_baseline', BitRate_Netflix, Rates_Netflix)
            
            del q, model, alpha, beta, u, j, r, s

    ###-------------------------------------------------###
    ###            Create saving file   (D)             ###
    ###-------------------------------------------------###

    ### Optimization based only on BW constraints - no user interactivity

    print(name_file + '_' + videoName_all[0] + '_Apple_baseline')
    scenario =  directory + '/' + videoName_all[0] + '_Apple_real'

    if not os.path.exists(directory):
        os.makedirs(directory)
        
        ##To write results
        csvData = ['VideoName', 'ch #','Tiles #', 'Rate Val.', 'sp #', 'Tile Res']
        
        with open(scenario + '_OptResults.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(csvData)
        csvFile.close()

    with open(scenario + '_Scenario.txt', 'w') as alphaFile:
        alphaFile.write('#VideoName u p(u) Dev p(d) Network p(n) BW p(BW) mu_e mu_s lambda_cost CostMax\n')
        alphaFile.close()
        
        with open(scenario + '_OptResults_alpha.txt', 'w') as alphaFile:
            alphaFile.write('#VideoName idx_ch idx_Tiles Quality idx_sp u p(j) Distortion RateVal TileRes(W) TileRes(H) \n')
        alphaFile.close()

    with open(scenario + '_OptResults_beta.txt', 'w') as betaFile:
        betaFile.write('#VideoName idx_ch idx_Tiles Quality idx_sp RateVal TileRes(W) TileRes(H) Distortion(Dev_1) Distortion(Dev_2) Distortion(Dev_3)\n')
        alphaFile.close()
        
        with open(scenario + '_OptResults_objValues.txt', 'w') as ObjFile:
            ObjFile.write('#VideoName idx_ch objVal(TOT) objVal1 objVal2(enc) objVal3(stor) \n')
        ObjFile.close()

    ###-------------------------------------------------###
    ###               Solve SCENARIO (D) baseline                ###
    ###-------------------------------------------------###


    for videoName in videoName_all:
        for ch in range(n_ch):
            
            print('Chunk = ' + str(ch))
            # The prob variable is created to contain the problem data
            model = pulp.LpProblem("Server Optimization",pulp.LpMinimize)
                
                
            # Decision variables: (they need string as input variable)
            alpha = pulp.LpVariable.dicts("Alpha_DecVar",(Users,Tiles,Rates_Apple,sp_index),0,1,pulp.LpInteger)
            beta = pulp.LpVariable.dicts('Beta_DecVar',(Tiles,Rates_Apple,sp_index),0,1,pulp.LpInteger)
            gamma = pulp.LpVariable.dicts('Gamma_DecVar',(Users,sp_index),0,1,pulp.LpInteger)
            
            #tile prob from heatmap for the chunk
            prob = tiles_prob(videoName, ch)
            
            q = read_RD(videoName,  Rates_Apple, ch, '_Apple')
            
            model += pulp.lpSum([q[int(u)][int(j)][int(r)][int(Res_Apple[int(r)])]*alpha[u][j][r][Res_Apple[int(r)]]*S_tiles[int(j)]*Users_cat.Prob_u[int(u)] for u in Users for j in Tiles for r in Rates_Apple for s in sp_index]),"Obj fun"
            
            ### ---- constraints ----
            ### --- a) set up decision variable alpha
            # A constraint ensuring that only one value can be in each square is created
            for u in Users:
                for j in Tiles:
                    model += pulp.lpSum([alpha[u][j][r][s] for r in Rates_Apple for s in sp_index]) == 1, ""
            print("Constraint A - done")
            
            for s in sp_index:
                for j in Tiles:
                    model += pulp.lpSum([beta[j][r][s] for r in Rates_Apple]) >= 1, ""
                    
            for u in Users:
                model += pulp.lpSum([gamma[u][s] for s in sp_index]) <= 1, ""
    
        #       ### --- b) set up decision variable alpha  and beta
            for u in Users:
                for s in sp_index:
                    for j in Tiles:
                        for r in Rates_Apple:
                            model += alpha[u][j][r][s] <= beta[j][r][s], ''
                            model += alpha[u][j][r][s] <= gamma[u][s] , ''
            print("Constraint B - done")


            for s in sp_index:
                for j in Tiles:
                    for r in Rates_Apple:
                        model += beta[j][r][s] <= pulp.lpSum([alpha[u][j][r][s] for u in Users]),""
            
            ### --- c) set up decision variable beta & alpha
            print("Constraint C - done")
            
            for u in Users:
                for s in sp_index:
                    model += gamma[u][s] <= pulp.lpSum([alpha[u][j][r][s] for j in Tiles for r in Rates_Apple]),""

    
                    
            ### --- d) set up bw constraints
            for u in Users:
                model += pulp.lpSum([alpha[u][j][r][s]*BitRate_Apple[int(r)] for r in Rates_Apple for j in Tiles for s in sp_index]) <= Users_cat.BW_u[int(u)], ""
            print("Constraint D - done")

            for u in Users:
                for j in Tiles:
                    for r in Rates_Apple:
                        for s in sp_index:
                            if int(s) == int(Res_Apple[int(r)]):
                                model += alpha[u][j][r][s] <= 1 , ''
                            else:
                                model += alpha[u][j][r][s] == 0 , ''
            
            for u in Users:
                for j in Tiles:
                    for s in sp_index:
                        if Devices[int(s)] == Users_cat.Device[int(u)]:
                            model += pulp.lpSum([alpha[u][j][r][s] for r in Rates_Apple]) == 1
                        else:
                            model += pulp.lpSum([alpha[u][j][r][s] for r in Rates_Apple]) == 0
            
            model.solve()
            
            print_Results_opt('Apple_baseline', BitRate_Apple, Rates_Apple)
            
            del q, model, alpha, beta,u, j, r, s

    print('Finish optimization')
        
if __name__ == '__main__':
    main() 
    

'''
Akond Rahman 
Mar 19, 2019 : Tuesday 
ACID: Main 
'''
import excavator
import constants


if __name__=='__main__':

    # orgName='wikimedia-downloads'
    # out_fil_nam = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/WIKI_PUPP_COMM.PKL'

    # orgName='openstack-downloads'
    # out_fil_nam = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/OSTK_PUPP_COMM.PKL'

    fileName     = constants.ROOT_PUPP_DIR + orgName + '/' + constants.REPO_FILE_LIST 
    elgibleRepos = excavator.getEligibleProjects(fileName)
    dic = {}
    for proj_ in elgibleRepos:
        proj_data = excavator.runMiner(orgName, proj_, constants.MASTER_BRANCH)
        dic[proj_] = proj_data

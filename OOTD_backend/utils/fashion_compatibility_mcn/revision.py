import os
import warnings

import matplotlib; matplotlib.use('agg')
import matplotlib.pyplot as plt
import torch
from PIL import Image
from utils.fashion_compatibility_mcn.diagnosis import *
import random
warnings.filterwarnings('ignore')
plt.rc('font',family='Times New Roman')
from utils.fashion_compatibility_mcn.model import CompatModel
os.environ['TORCH_HOME'] = '/code/utils/fashion_compatibility_mcn'
def retrieve_sub(x, select, order, all_path, model):
    """ Retrieve the datset to substitute the worst item for the best choice.
    """
    all_names = {0:'upper', 1:'bottom', 2:'shoes', 3:'bag', 4:'accessory'}

    best_score = -1
    best_img_path = dict()
    img_idx = dict()
    for o in order:
        if best_score > 0.9:
            break
        problem_part_idx = select[o]
        problem_part = all_names[problem_part_idx]
        outfit_idx = 0
        for outfit in all_path[problem_part]:
            print("outfit:",outfit)
            if best_score > 0.9:
                break
            img_path = os.path.join("media/images/", outfit)
            img = transform(Image.open(img_path).convert('RGB')).to(device)
            x[0][problem_part_idx] = img
            with torch.no_grad():
                score, *_ = model._compute_score(x)
            if score.item() >= best_score:
                best_score = score.item()
                best_img_path[problem_part] = img_path
                img_idx[problem_part] = outfit_idx
                print("best:",best_img_path)
            outfit_idx+=1
        x[0][problem_part_idx] = transform(Image.open(best_img_path[problem_part]).convert('RGB')).to(device)
        #print('problem_part: {}'.format(problem_part))
        #print('best substitution: {}'.format(best_img_path[problem_part]))
        #print('After substitution the score is {:.4f}'.format(best_score))
        # plt.imshow(plt.imread(best_img_path[problem_part]))
        # plt.gca().axis('off')
        # plt.show()
    
    #after = show_imgs(x[0], select, "revised_outfit.png")
    return best_score, best_img_path,img_idx

def generate_outfit(path,model):
    all_names = ['bottom','shoes','bag','accessory']
    select = [0]
    best_score = -1
    best_img_path = dict()
    img_path_idx = dict()
    img_path_idx["upper"] = random.randint(0,len(path["upper"])-1)
    #print(img_path_idx)
    best_img_path['upper'] = path['upper'][img_path_idx["upper"]]
    x = loadimg_from_path([best_img_path['upper'],"bottom_mean","shoes_mean","bag_mean","accessory_mean"])
    idx=0
    for name in all_names:
        idx+=1
        have_better = False
        outfit_idx = 0
        for outfit in path[name]:
            img_path = os.path.join("media/images/", outfit)
            img = Image.open(img_path).convert('RGB')
            img = transform(img).to(device)
            x[0][idx]=img
            with torch.no_grad():
                score, *_ = model._compute_score(x)
            if score.item() > best_score:
                have_better = True
                best_score = score.item()
                best_img_path[name]=img_path
                img_path_idx[name]=outfit_idx
            outfit_idx+=1
        if have_better:
            select.append(idx)
            x[0][idx] = transform(Image.open(best_img_path[name]).convert('RGB')).to(device)
        else:
            x[0][idx] = transform(Image.open("utils/data/"+name+".png").convert('RGB')).to(device)
            best_img_path.setdefault(name, "utils/data/"+name+".png")  # 设置默认值

    #show_imgs(x[0], select, "generated_outfit.png")
    #print('score is {:.4f}'.format(best_score))
    #print(img_path_idx)
    return best_score,best_img_path,img_path_idx

def evaluate(path,model,all_path):
    x = loadimg_from_path(path).to(device)
    select = [i for i, l in enumerate(path) if 'mean' not in l]
    #before = show_imgs(x[0], select)
    relation, rate = defect_detect(x, model)
    relation = relation.squeeze().cpu().data
    #show_rela_diagnosis(relation, select, cmap=plt.cm.Blues)
    result, order = item_diagnosis(relation, select)
    best_score, best_img_path,img_idx = retrieve_sub(x, select, order,all_path, model)
    replace = (best_score != rate)
    return rate, replace, best_score, best_img_path,img_idx
    


def preprocess():
    model = CompatModel(embed_size=1000, need_rep=True, vocabulary=2757).to(device)
    
    model.load_state_dict(torch.load('/code/utils/fashion_compatibility_mcn/model_train_relation_vse_type_cond_scales.pth',map_location=torch.device('cpu')))
    model.eval()
    return model
    

if __name__ == "__main__":
    # Load model weights
    model = preprocess()
    path = ["../data/images/up/up1.jpg","../data/images/bottom/bottom1.jpg","../data/images/shoes/shoes1.jpg","bag_mean","../data/images/accessory/hat1.jpg"]
    all_path = {
    'upper':["up/up1.jpg","up/up2.jpg","up/dress.jpg","up/fengyi.jpg"],
    'bottom':["bottom/bottom1.jpg","bottom/bottom2.jpg","bottom/blackpants.jpg"],
    'shoes':["shoes/shoes1.jpg","shoes/shoes2.jpg","shoes/nike.jpg","shoes/highheel.jpg"],
    'bag':["bag/bag1.jpg","bag/bag2.jpg"],
    'accessory':["accessory/hat1.jpg","accessory/hat2.jpg"]
    }
    #score(path,model,all_path)
    generate_outfit(all_path,model)
    """
    model = CompatModel(embed_size=1000, need_rep=True, vocabulary=2757).to(device)
    model.load_state_dict(torch.load('./model_train_relation_vse_type_cond_scales.pth',map_location=torch.device('cpu')))
    model.eval()

    best_score,best_img_path = generate_outfit(all_path)

   
    print("="*80)
    path = ["../data/images/up/up1.jpg","../data/images/bottom/bottom1.jpg","../data/images/shoes/shoes1.jpg","bag_mean","../data/images/accessory/hat1.jpg"]
    x = loadimg_from_path(path).to(device)
    select = [i for i, l in enumerate(path) if 'mean' not in l]
    print("Step 1: show images in an outfit...")
    show_imgs(x[0], select)

    print("\nStep 2: show diagnosis results...")
    relation, out = defect_detect(x, model)
    relation = relation.squeeze().cpu().data
    show_rela_diagnosis(relation, select, cmap=plt.cm.Blues)
    result, order = item_diagnosis(relation, select)
    print("Predicted Score: {:.4f}\nProblem value of each item: {}\nOrder: {}".format(out, result, order))

    print("\nStep 3: substitute the problem items for revision, it takes a while to search...")
    best_score, best_img_path = retrieve_sub(x, select, order)
    print("="*80)
    """
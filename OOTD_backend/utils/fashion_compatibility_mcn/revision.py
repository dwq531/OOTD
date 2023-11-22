import os
import warnings

import matplotlib; matplotlib.use('agg')
import matplotlib.pyplot as plt
import torch
from PIL import Image
from diagnosis import *
import random
warnings.filterwarnings('ignore')
plt.rc('font',family='Times New Roman')

def retrieve_sub(x, select, order):
    """ Retrieve the datset to substitute the worst item for the best choice.
    """
    all_names = {0:'upper', 1:'bottom', 2:'shoe', 3:'bag', 4:'accessory'}

    best_score = -1
    best_img_path = dict()

    for o in order:
        if best_score > 0.9:
            break
        problem_part_idx = select[o]
        problem_part = all_names[problem_part_idx]
        #print("problem part:",problem_part)
        for outfit in all_path[problem_part]:
            #print("outfit:",outfit)
            if best_score > 0.9:
                break
            img_path = os.path.join("../data/images/", outfit)
            img = transform(Image.open(img_path).convert('RGB')).to(device)
            x[0][problem_part_idx] = img
            with torch.no_grad():
                score, *_ = model._compute_score(x)
            if score.item() >= best_score:
                best_score = score.item()
                best_img_path[problem_part] = img_path
                #print("best:",best_img_path)
        x[0][problem_part_idx] = transform(Image.open(best_img_path[problem_part]).convert('RGB')).to(device)
        #print('problem_part: {}'.format(problem_part))
        #print('best substitution: {}'.format(best_img_path[problem_part]))
        print('After substitution the score is {:.4f}'.format(best_score))
        # plt.imshow(plt.imread(best_img_path[problem_part]))
        # plt.gca().axis('off')
        # plt.show()
    
    show_imgs(x[0], select, "revised_outfit.png")
    return best_score, best_img_path

def generate_outfit(path):
    all_names = ['bottom','shoe','bag','accessory']
    select = [0]
    best_score = -1
    best_img_path = dict()
    img_path_idx = random.randint(0,len(path["upper"])-1)
    #print(img_path_idx)
    best_img_path['upper'] = os.path.join("../data/images/",path['upper'][img_path_idx])
    x = loadimg_from_path([best_img_path['upper'],"../data/bottom.png","../data/shoe.png","../data/bag.png","../data/accessory.png"])
    idx=0
    for name in all_names:
        idx+=1
        have_better = False
        for outfit in path[name]:
            img_path = os.path.join("../data/images/", outfit)
            img = Image.open(img_path).convert('RGB')
            img = transform(img).to(device)
            x[0][idx]=img
            with torch.no_grad():
                score, *_ = model._compute_score(x)
            if score.item() > best_score:
                have_better = True
                best_score = score.item()
                best_img_path[name]=img_path
                #print("best:",best_img_path)
        if have_better:
            select.append(idx)
            x[0][idx] = transform(Image.open(best_img_path[name]).convert('RGB')).to(device)
        else:
             x[0][idx] = transform(Image.open("../data/"+name+".png").convert('RGB')).to(device)

    show_imgs(x[0], select, "generated_outfit.png")
    print('score is {:.4f}'.format(best_score))
    return best_score,best_img_path

if __name__ == "__main__":
    # Load model weights
    from model import CompatModel
    model = CompatModel(embed_size=1000, need_rep=True, vocabulary=2757).to(device)
    model.load_state_dict(torch.load('./model_train_relation_vse_type_cond_scales.pth',map_location=torch.device('cpu')))
    model.eval()

    best_score,best_img_path = generate_outfit(all_path)

   
    print("="*80)
    path = ["../data/images/up/up2.jpg","../data/images/bottom/bottom1.jpg","../data/images/shoes/shoes1.jpg","bag_mean","../data/images/accessory/hat2.jpg"]
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
    
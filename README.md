# Assessing Streetscape Quality Related to Pedestrian Crashes Using Supervised Learning

**Course:** URSP688Y
**Term:** Spring 2025  

**Author:**  
Huan Zhou  
[hzhou715@umd.edu](mailto:hzhou715@umd.edu)

**Instructor:**  
Dr. Chester Harvey  
National Center for Smart Growth  
[cwharvey@umd.edu](mailto:cwharvey@umd.edu)

---

## 1. Project overview

This project investigates the use of supervised learning to assess streetscape quality related to pedestrian crashes. By leveraging Google Street View images, AI-based automated labeling and Vertex AI's Auto Machine Learning, the project aims to evaluate streetscape quality at scale.

Supervised learning in this context involves training a model using pseudo-labeled data (generated via ChatGPT 4.1), followed by fine-tuning using a smaller set of manually labeled ground truth data. This approach allows the model to learn visual features with minimal human annotation, improving scalability and efficiency.

---

## 2. Data and methodology

### 2.1 Data sources

- **Street View Images:** 1,300 images from Baltimore City, collected via the Google Maps Street View API.
- **Train/Validation Set:** 1,100 pseudo-labeled images (using ChatGPT 4.1), split 10/1 for training and validation.
- **Test Set:** 100 manually annotated images, used for final model evaluation.

### 2.2 Methods

The analytical process includes the following key steps:

1. **Download street view images**  
   Downloading street view image using the Google Maps API, focusing on areas with high pedestrian crash rates in Baltimore City.

2. **Label street view images**  
   - Pseudo-labeling for training using ChatGPT-based automation  
   - Manual annotation for test images to ensure high-quality ground truth

3. **Train the model**  
   A supervised model is pretrained using pseudo-labeled data, and then fine-tuned on ground truth labels using Vertex AI’s AutoML platform for multi-label classification.

4. **Evaluate**  
   Model performance is assessed using average precision, precision, and recall across the confidence threshold of 0.5.

---

## 3. Results

### Overall performance

- **Average Precision (AuPRC):** 0.687  
- **Precision:** 68.5%  
- **Recall:** 67.4%
- **Confidence threshold:** 0.5

### Per-Label precision scores

| Label                                 | Precision |
|--------------------------------------|-----------|
| presence_of_sidewalk_no              | 1.000     |
| presence_of_sidewalk_yes             | 1.000     |
| crosswalk_presence_no                | 0.919     |
| crosswalk_presence_yes               | 0.796     |
| presence_of_sidewalk_buffer_zone_yes | 0.787     |
| traffic_signs_yes                    | 0.760     |
| traffic_signs_no                     | 0.759     |
| streetlight_presence_yes             | 0.708     |
| sidewalk_condition_good              | 0.662     |
| streetlight_presence_no              | 0.638     |
| presence_of_sidewalk_buffer_zone_no  | 0.548     |
| road_pavement_condition_good         | 0.438     |
| road_pavement_condition_fair         | 0.406     |
| sidewalk_condition_poor              | 0.376     |
| road_pavement_condition_poor         | 0.346     |
| sidewalk_condition_fair              | 0.310     |

The model performs well in identifying visible features (e.g., sidewalks, crosswalks), but shows lower performance for subjective conditions (e.g., road pavement quality). These findings support the potential of automated image analysis for infrastructure screening while highlighting the need for human oversight in complex or subjective assessments.

---
## 4. Theoretical strengths and weeknesses

This study demonstrates the strengths of using AI for scalable, objective assessment of streetscape quality. By using street view imagery and Auto Machine Learning, public agencies can efficiently identify infrastructure disparities, such as missing sidewalks or absent crosswalks. In this way, data science offers a method to detect and prioritize low-quality environments that may affect underserved communities. This aligns with the goals of environment justice, where the quality of the built environment should not determine one’s risk exposure.

However, limitations arise from both the models and data. The model performs well in detecting visible infrastructure but struggles with subjective assessments such as pavement or sidewalk condition. It cannot capture condition-based inequities. Moreover, the dataset is biased. Street view images coverage is more frequent in downtown, while underserved neighborhoods or rural areas may have outdated or no images. The places most in need of investment may be least represented in the training data.

In summary, while AI enables large scale audits of streetscape quality, it lacks human insight and sufficient representation of vulnerable areas. Future work should integrate community cooperation and diverse datasets to ensure smart city tools improve rather than undermine urban equity.


## 5. Project structure and file descriptions

The project is organized into three primary stages: downloading street view images, labeling, and training the model. Each stage is organized in its own folder, along with supporting code and datasets.

```
├── 1_download_street_view/                 # Scripts and files for acquiring street view images  
│   ├── 100point_network_test.csv           # Coordinates of sample points along road network  
│   ├── 100points_panoid_results.csv        # Panoid results matched to sample points  
│   ├── panoid_unique_latest_date.csv       # Cleaned list of unique panoids with latest dates  
│   ├── panoid_unique_latest_date.py        # Script for extracting latest panoid per sample point  
│   └── download_gsv.py                     # Code to download images using Google Street View API  
│
├── 2_label_street_view/                    # Labeling process (ChatGPT-based and manual)  
│   └── chatgpt_label.py                    # Script to auto-label images using ChatGPT  
│
├── 3_train_model/                          # Image data prepared for training in Vertex AI  
│   ├── train_dataset_sample/               # Folder of training images (pseudo-labeled) 
│   ├── test_dataset_sample/                # Folder of test images (ground truth)  
│   ├── train_labels_chatgpt41.csv          # Pseudo-labels generated for training  
│   └── test_labels_ground_truth.csv        # Manually labeled ground truth for test  
│
├── method_explanation.ipynb                # Main notebook explaining project methodology  
├── Narrative.pdf                           # Final narrative report for the project  
└── README.md                               # Finalized project README  
```




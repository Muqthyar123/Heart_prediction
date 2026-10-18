# HeartPredict AI

I want you to build a complete, modern, clean, responsive, and attractive frontend website for my machine-learning project called:

"Advanced Heart Disease Prediction System"

The website is a frontend for an ML-based heart disease prediction system. It should look like a professional healthcare/AI product rather than a basic college project.

IMPORTANT:

Do not create a generic medical dashboard. The UI should be specifically designed around my Advanced Heart Disease Prediction project.

==================================================

1. PROJECT OVERVIEW

==================================================

The system predicts heart disease risk using patient clinical information and machine-learning models.

The project uses 13 input features:

1. Age

2. Sex / Gender

3. Chest Pain Type (cp)

4. Resting Blood Pressure (trestbps)

5. Serum Cholesterol (chol)

6. Fasting Blood Sugar (fbs)

7. Resting ECG (restecg)

8. Maximum Heart Rate Achieved (thalach)

9. Exercise-Induced Angina (exang)

10. ST Depression (oldpeak)

11. ST-Segment Slope (slope)

12. Number of Major Vessels (ca)

13. Thalassemia (thal)

The target is the heart-disease prediction class.

The ML project includes multiple models:

- Logistic Regression

- Random Forest

- Support Vector Machine (SVM)

- K-Nearest Neighbors (KNN)

- Decision Tree

- Naive Bayes

- AdaBoost

- Neural Network / MLP

- XGBoost

- LightGBM

- CatBoost

- Extra Trees

- Hybrid Stacking Classifier

The main hybrid approach combines:

Random Forest + SVM + KNN

        ↓

Logistic Regression Meta Learner

        ↓

Final Prediction

The website should present this project clearly without overwhelming the user with technical information.

==================================================

2. TECHNOLOGY

==================================================

Use:

- React

- TypeScript

- Tailwind CSS

- Modern component-based architecture

- React Router for page navigation

- Lucide React or another modern icon library

- Reusable components

- Responsive design for desktop, tablet and mobile

Keep the code clean and production-quality.

Create a proper folder structure with:

components/

pages/

layouts/

services/

types/

utils/

assets/

Separate reusable components from page-specific components.

==================================================

3. WEBSITE STRUCTURE

==================================================

Create the following main pages:

1. Home

2. About

3. Single Prediction

4. Bulk Prediction

5. Lifestyle Risk

Navigation should be visible in a modern navbar.

Navbar:

- Logo / brand name:

  "HeartPredict AI"

- Home

- About

- Single Prediction

- Bulk Prediction

- Lifestyle Risk

- A prominent "Predict Now" button

On mobile, use a hamburger menu.

==================================================

4. DESIGN DIRECTION

==================================================

The website must be:

- Clean

- Modern

- Professional

- Attractive

- Responsive

- Accessible

- Easy to understand

- Healthcare + AI themed

Use a sophisticated medical/AI visual language.

Avoid:

- Excessive gradients

- Overly bright colors

- Too many animations

- Cluttered dashboards

- Huge amounts of text

- Cartoonish medical graphics

Use:

- Clean cards

- Rounded corners

- Subtle shadows

- Good typography

- Proper spacing

- Clear visual hierarchy

- Soft healthcare-inspired colors

- Professional icons

- Subtle animations

- Hover states

- Loading states

- Empty states

- Error states

The website should feel similar to a modern SaaS/healthcare application.

Use a consistent design system across all pages.

==================================================

5. HOME PAGE

==================================================

Create an attractive landing page.

Hero section:

Headline:

"Advanced Heart Disease Prediction"

Subheadline:

"Analyze clinical and lifestyle factors with machine learning to estimate heart disease risk."

Primary CTA:

"Start Prediction"

Secondary CTA:

"Explore the Project"

Hero visual:

Create a modern AI + healthcare visual using cards/icons rather than a generic stock photo.

Show a visual representation such as:

Patient Data

      ↓

AI Analysis

      ↓

Risk Prediction

Add subtle animations.

Below the hero, create a statistics/features section.

Example cards:

"13"

Clinical Features

"13+"

ML Models Evaluated

"Hybrid"

Stacking Architecture

"AI-Powered"

Risk Prediction

Do not invent accuracy values. If exact model accuracy is not available from the backend, do not display fake accuracy.

==================================================

6. HOME PAGE FEATURES SECTION

==================================================

Create a section titled:

"Multiple Ways to Assess Risk"

Create three feature cards:

A. Single Patient Prediction

"Enter one patient's clinical information and receive an individual prediction."

Button:

"Predict for One"

B. Bulk Prediction

"Upload an Excel file containing multiple patient records and generate predictions in bulk."

Button:

"Analyze Multiple"

C. Lifestyle Risk Assessment

"Answer lifestyle-related questions to receive a lifestyle-based risk assessment."

Button:

"Assess Lifestyle Risk"

Each card should have a suitable icon.

==================================================

7. HOME PAGE WORKFLOW

==================================================

Create a section:

"How It Works"

Show a 4-step visual workflow:

01

Enter Patient Data

02

Preprocess Features

03

AI Model Analysis

04

Risk Prediction

Use a horizontal timeline on desktop and vertical timeline on mobile.

==================================================

8. ABOUT PAGE

==================================================

Create a detailed but visually clean About page.

Sections:

1. Project Overview

2. Problem Statement

3. Objective

4. Dataset

5. Input Features

6. Data Preprocessing

7. Machine Learning Models

8. Hybrid Stacking Architecture

9. Feature Importance

10. Model Evaluation

11. Real-World Application

12. Limitations

13. Future Scope

==================================================

9. ABOUT — INPUT FEATURES

==================================================

Display the 13 clinical features in a clean grid/table.

Use these names:

Age

Sex

Chest Pain Type

Resting Blood Pressure

Serum Cholesterol

Fasting Blood Sugar

Resting ECG

Maximum Heart Rate

Exercise-Induced Angina

ST Depression

ST-Segment Slope

Number of Major Vessels

Thalassemia

For each feature, show:

- Feature name

- Dataset code

- Short explanation

- Input type

Example:

Age

Code: age

Type: Numerical

Description: Patient age in years

Chest Pain Type

Code: cp

Type: Categorical

Description: Type of chest pain reported by the patient

==================================================

10. ABOUT — PREPROCESSING

==================================================

Explain the ML preprocessing pipeline visually:

Raw Data

↓

Missing Value Handling

↓

Outlier Detection

↓

Categorical Encoding

↓

Feature Scaling

↓

Train/Test Data

↓

Model Training

Mention that the project uses:

- Median imputation

- IQR-based outlier handling

- Encoding

- StandardScaler

- Stratified splitting

Do not claim preprocessing steps that are not part of the actual project.

==================================================

11. ABOUT — MODEL ARCHITECTURE

==================================================

Create an attractive interactive model architecture diagram.

Show:

                 Patient Data

                      |

                      v

              Preprocessing

                      |

          +-----------+-----------+

          |           |           |

          v           v           v

     Random Forest   SVM         KNN

          |           |           |

          +-----------+-----------+

                      |

                      v

             Logistic Regression

                Meta Learner

                      |

                      v

              Final Prediction

Also show the other implemented models separately as a model comparison grid:

Logistic Regression

Random Forest

SVM

KNN

Decision Tree

Naive Bayes

AdaBoost

MLP

XGBoost

LightGBM

CatBoost

Extra Trees

Stacking

==================================================

12. FEATURE IMPORTANCE

==================================================

Create a visual feature importance section based on the project's feature importance analysis.

The top features shown in the project include:

cp

thalach

ca

oldpeak

thal

age

chol

trestbps

exang

slope

Create a horizontal bar chart.

Use the approximate importance values from the project's feature importance figure only if they are actually available.

Do not invent values for the missing features.

Explain:

"Feature importance indicates how strongly individual features contribute to the model's predictive decisions."

==================================================

13. SINGLE PREDICTION PAGE

==================================================

This is one of the most important pages.

Create a professional patient prediction form.

Title:

"Single Patient Prediction"

Subtitle:

"Enter the patient's clinical information to generate a heart disease prediction."

Organize the form into logical sections.

SECTION 1:

Basic Information

- Age

- Sex

SECTION 2:

Cardiac Information

- Chest Pain Type

- Resting Blood Pressure

- Serum Cholesterol

- Fasting Blood Sugar

- Resting ECG

- Maximum Heart Rate

- Exercise-Induced Angina

SECTION 3:

Exercise / Clinical Indicators

- ST Depression

- ST-Segment Slope

- Number of Major Vessels

- Thalassemia

Use appropriate controls:

- Number input for numerical values

- Select/dropdown for categorical features

- Toggle/radio buttons for binary features

- Sliders where appropriate

Do NOT make users type categorical codes manually.

For example:

Instead of:

Chest Pain Type = 0/1/2/3

display human-readable options and internally map them to the correct model values.

==================================================

14. SINGLE PREDICTION FORM VALIDATION

==================================================

Add frontend validation.

Examples:

- Age cannot be negative

- Blood pressure cannot be negative

- Cholesterol cannot be negative

- Heart rate cannot be negative

- Required fields must be completed

Show clear inline validation messages.

Prevent submission when required data is invalid.

==================================================

15. SINGLE PREDICTION RESULT

==================================================

After clicking:

"Predict Heart Disease Risk"

show a beautiful result card.

Possible states:

- Lower predicted risk / negative class

- Higher predicted risk / positive class

Do not use wording that implies medical diagnosis.

Use wording such as:

"Model Prediction"

and:

"This result is a machine-learning prediction and should not replace professional medical evaluation."

Show:

Prediction

Risk indicator

Confidence/probability if returned by backend

Model used

If the backend returns probability, display it using a clean circular progress/risk indicator.

If the backend does not return probability, do not fabricate one.

Include buttons:

"Predict Again"

"View Details"

==================================================

16. BULK PREDICTION PAGE

==================================================

Create a dedicated page:

"Bulk Prediction"

Purpose:

Allow users to upload multiple patient records through:

- Excel (.xlsx / .xls)

- CSV if supported

- A folder containing multiple supported files, if backend supports folder upload

Main upload area:

Large drag-and-drop zone.

Text:

"Upload Patient Data"

"Drag and drop your Excel file here or browse from your computer."

Show accepted formats.

After upload:

Display:

- File name

- Number of records

- Number of features detected

- Upload status

Then validate whether the uploaded data contains the required 13 features.

Required columns:

age

sex

cp

trestbps

chol

fbs

restecg

thalach

exang

oldpeak

slope

ca

thal

If columns are missing:

show a clear error such as:

"Missing required columns: cp, thalach"

Do not allow prediction until the file structure is valid.

==================================================

17. BULK PREDICTION RESULTS

==================================================

After backend processing, show:

- Total patients

- Predicted positive

- Predicted negative

- Processing status

Create a results table:

Patient ID | Prediction | Risk/Probability | Status

Add:

- Search

- Filter

- Sort

- Pagination

Add summary cards:

Total Patients

Higher Risk

Lower Risk

Create a chart showing prediction distribution.

Provide:

"Download Results"

button.

Allow downloading the prediction results as Excel/CSV if backend supports it.

==================================================

18. LIFESTYLE RISK PAGE

==================================================

Create a separate page:

"Lifestyle Risk Assessment"

This page is different from the clinical prediction page.

Purpose:

Ask users questions about lifestyle and health-related habits and generate a lifestyle-based risk assessment.

Design it like a guided questionnaire rather than a long form.

Use multiple steps.

Example:

Step 1:

Physical Activity

Step 2:

Diet

Step 3:

Smoking / Tobacco

Step 4:

Alcohol

Step 5:

Sleep

Step 6:

Stress

Step 7:

Weight / General Health

Use:

- Radio buttons

- Selects

- Toggles

- Sliders

Do not make the questionnaire visually overwhelming.

Show a progress indicator:

Step 2 of 7

==================================================

19. LIFESTYLE RESULT

==================================================

After completing the questionnaire:

Show:

"Lifestyle Risk Assessment"

with a visual risk indicator.

Possible categories:

Lower Lifestyle Risk

Moderate Lifestyle Risk

Higher Lifestyle Risk

Clearly state:

"This is a lifestyle-based risk assessment and is not a medical diagnosis."

Show a breakdown such as:

Physical Activity

Diet

Smoking

Sleep

Stress

Use visual indicators.

Then show general recommendations such as:

- Maintain regular physical activity

- Follow a balanced diet

- Avoid smoking

- Maintain healthy sleep habits

- Manage stress

These should be presented as general wellness guidance, not medical treatment.

==================================================

20. RESPONSIVENESS

==================================================

The website must work properly on:

- Desktop

- Laptop

- Tablet

- Mobile

Desktop:

Use multi-column layouts.

Tablet:

Reduce columns appropriately.

Mobile:

Use single-column forms.

Tables should become horizontally scrollable or transform into responsive cards.

Navigation should become a mobile hamburger menu.

==================================================

21. UX DETAILS

==================================================

Add:

- Loading animations

- Skeleton loaders where useful

- Toast notifications

- Form validation

- Error states

- Empty states

- Upload progress

- Button disabled states

- Hover animations

- Smooth page transitions

- Accessible labels

- Keyboard navigation

Do not overuse animations.

==================================================

22. BACKEND/API INTEGRATION

==================================================

Build the frontend so it can connect to a Python ML backend later.

Assume REST API endpoints such as:

POST /predict

For single patient prediction.

POST /bulk-predict

For Excel/CSV bulk prediction.

POST /lifestyle-risk

For lifestyle assessment.

GET /health

For backend health checking.

Create a centralized API service such as:

services/api.ts

Do not put API calls directly inside UI components.

Use TypeScript interfaces for:

PatientInput

PredictionResponse

BulkPredictionResponse

LifestyleInput

LifestylePredictionResponse

For development, create mock API responses so the frontend can run even without the backend.

IMPORTANT:

Clearly separate mock data from actual API integration.

Do not hardcode fake model accuracy or fake prediction results.

==================================================

23. COMPONENTS

==================================================

Create reusable components such as:

Navbar

Footer

HeroSection

FeatureCard

StatCard

SectionHeader

FeatureTable

ModelCard

ModelArchitecture

PredictionForm

FormSection

InputField

SelectField

RiskIndicator

PredictionResult

FileUploader

UploadStatus

ResultsTable

ResultSummary

LifestyleQuestion

ProgressIndicator

RiskBreakdown

LoadingState

ErrorState

Toast

==================================================

24. HOME PAGE FOOTER

==================================================

Footer should contain:

HeartPredict AI

"Machine-learning based heart disease risk prediction."

Navigation links.

A disclaimer:

"This system is intended for research and decision-support purposes. Predictions should not be considered a medical diagnosis."

==================================================

25. IMPORTANT MEDICAL SAFETY

==================================================

Do not present the system as a doctor.

Do not say:

"100% accurate"

"Guaranteed diagnosis"

"This proves you have heart disease"

Instead use:

"Model Prediction"

"Estimated Risk"

"Prediction Result"

"Decision Support"

Always include a concise disclaimer.

==================================================

26. VISUAL QUALITY

==================================================

The final website should look like a real-world AI healthcare product.

The UI should have:

- Strong visual hierarchy

- Consistent spacing

- Professional typography

- Beautiful cards

- Clean charts

- Modern icons

- Responsive forms

- Clear CTA buttons

- Excellent empty/loading/error states

Make the prediction pages especially polished because they are the core functionality.

==================================================

27. CODE QUALITY

==================================================

Write production-quality code.

Requirements:

- TypeScript

- Reusable components

- No unnecessary duplication

- Proper state management

- Proper form validation

- Clean API abstraction

- Responsive Tailwind classes

- Meaningful variable names

- Comments only where useful

- No giant components

- No hardcoded API logic inside pages

==================================================

28. FINAL REQUIREMENT

==================================================

Build the complete frontend, not just a static design.

All navigation must work.

All pages must be accessible.

Forms must work with mock prediction responses if the backend is unavailable.

Bulk upload UI must work.

Lifestyle questionnaire must work.

Prediction result UI must work.

The final result should feel like a polished, real-world AI healthcare application.

Before finishing, check:

- Desktop responsiveness

- Mobile responsiveness

- Navigation

- Form validation

- Upload UI

- Prediction result states

- Error states

- Loading states

- Accessibility

- Consistent design

- No fake accuracy claims

- No broken routes

- No console errors

Start by creating the complete project structure and then implement each page and reusable component.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/6cda9ce3-f13d-4f45-aef2-be7be7511c73).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```

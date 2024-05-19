# Lmaghrib-BinYedik
![DALLE2024-05-1818 45 51-AbannerforaGitHubrepositoryforanapplicationcalledLmaghrib-BinYedikwhichguidestouristsinMorocco ThedesignshouldfeatureMoroccancul-ezgif com-webp-to-jpg-converter](https://github.com/Tensor-Titans/Lmaghrib-BinYedik/assets/49345542/5ee03377-1f54-4fac-bb4e-1a252fec07d9)

 
### Lmaghrib-BinYedik is a pioneering project developed during the 2024 ThinkAI GenAI Hackathon under the theme of tourism. Our application integrates extensive information about Moroccan monuments into a single, user-friendly chatbot platform, offering tourists a seamless and enriching travel experience.

 ## We Offer:

- **Comprehensive Information**:  Access in-depth descriptions, historical data, and fascinating narratives about Morocco's iconic monuments.
- **Navigation Assistance**: Utilize precise directions and interactive maps to navigate through Moroccan cities effortlessly.
- **Pricing Details**: Stay informed with the latest entry fees for monuments, local food prices, and other essential costs.
- **User Support**: Receive expert travel tips and real-time assistance to make the most out of your journey in Morocco.





## Strategy and Execution

### Task 1 : Monument Identification

To enhance the accuracy of monument recognition, we evaluated various models before selecting the Google Lens API for its superior performance in handling diverse image data:


| Model     | Accuracy                          | Flexibility |  Chosen | 
|-----------|-----------------------------------|-----------|------| 
| YoloV8 Classification     | High| Low (limited number of classes) |❌ |
| Bing Reverse Search | Average     | Average (doesn't work too well with new data) |❌ |
| Google Lens      | High              | High   |✅|


Using the Google Lens API, we capture a broad spectrum of images related to each monument. The LLaMA3 LLM then processes this data, efficiently identifying the exact monument name from the image attributes. We selected the 8 billion parameter model of LLaMA3 for its balance of speed and accuracy, crucial for real-time application needs.






### Task 2 : Information Retriever

With the monument identified, LLaMA3 adopts a dual role:

Interactive Query Handling: Acts as a responsive agent to field questions about the monument, delivering detailed and accessible information.
Data Integration and Management: Leveraging LangGraph, we design complex, stateful interaction chains that maintain conversational context, enhancing user interaction continuity.


| Technique   | Accuracy                       | Speed    | Relevancy | Chosen |
|-----------|-----------------------------------|-----------|--------|--------|
| Llama3 Knowledge     | High| Fast (doesn't need extra steps to get data) | Low  |❌ |
| WebSearch | High     | Slow  | High|✅ |

Based on the data retrieved we format it into a suitable format that we can display into the GUI as a markdown with interactive links.

### Task 3 : Scam prevention for tourists

Addressing common tourist challenges, we focused on preventing overpayment scams by integrating a reliable pricing guide based on real-time data from scraped local sources like Marjane catalogs.


| Technique   | Accuracy                       | Speed    | Relevancy | Dependant on Dataset | Chosen |
|-----------|-----------------------------------|-----------|--------|--------|--------|
| Llama3 Knowledge     | Medium| Fast (doesn't need extra steps to get data) | Low  |No |❌ |
| Llama3 Prompt Engineered  | High(But can only take a small subset of dataset) | Slow (It uses up token for taking the data as context) | High  |Yes |❌ |
| WebSearch | High     | Slow  | High |No |✅ |
| Gemini FineTuned | High     | Average | Medium  |Yes |✅ |
| CsvAgent | Medium     |Fast  | Low (Needs Exact Name ) |Yes |❌ |




## Additional Features :

### Generating map links.
#### History Persistence: Ensures continuity in user interactions.
#### Context Relevancy: Keeps conversations relevant and engaging.
#### On_Chat_Resume: Allows users to pick up where they left off.
#### Authentication Mechanism: Secures user data and customizes experiences.
#### Multiple Model Profiles: Offers tailored responses based on user preferences.



Our implementation of LLaMA3 for Lmaghrib-BinYedik presents distinct advantages over cutting-edge models like GPT-4.
while GPT-4 offers broad general knowledge, LLaMA3 has been tailored to excel in domain-specific tasks, such as identifying and providing detailed information on Moroccan monuments. This focus ensures that our model not only provides accurate information but does so with a depth of understanding and contextual relevance that is specifically optimized for the tourism sector in Morocco.

![gpt4](https://github.com/Tensor-Titans/Lmaghrib-BinYedik/assets/77627747/ee42892b-9ee8-46c9-9203-33c8439184b0)


## Demo :


https://github.com/Tensor-Titans/Lmaghrib-BinYedik/assets/77627747/8a44fbf5-cb2f-4ee0-acaf-8320f5bddb0c






![identify our historical monuments](https://github.com/Tensor-Titans/Lmaghrib-BinYedik/assets/77627747/450391c4-8fd3-4d6c-b86a-dcb340880eba)




## Prerequisites

- Python 3.12.0 or newer

- 
## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Tensor-Titans/Lmaghrib-BinYedik.git
    cd Lmaghrib-BinYedik
    ```
3. **Create and Activate virtual environments:**
    ```sh
    # Create virtual environment
    python -m venv env
    
    # Activate virtual environment (Windows)
    .\env\Scripts\activate

    # Activate virtual environment (MacOS/Linux)
    source env/bin/activate
    ```

3. **Install dependencies:**
    ```sh
     pip install -r requirements.txt
    ```

## Running the Project

1. **Start the server:**
    ```sh
    chainlit run app.py -w
    ```

2. **Access the application:**
    Open your browser and go to http://localhost:8000/

## Running Tests
## Have Fun!

Explore the app, try out all the features, and enjoy discovering all the amazing information about Moroccan monuments, cuisine, and more!
## Data Sources

- [Moroccan Product Prices Data](https://drive.google.com/file/d/16JutKB5cA__95UHBk9OS5aGAPdsFvdyq/view?usp=sharing)

- [MonumentsMar Dataset](https://drive.google.com/file/d/11v6-1MtI4BCHFyILfAHhP9Ca9RZz9Tc-/view?usp=sharing)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

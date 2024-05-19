# Lmaghrib-BinYedik
![DALLE2024-05-1818 45 51-AbannerforaGitHubrepositoryforanapplicationcalledLmaghrib-BinYedikwhichguidestouristsinMorocco ThedesignshouldfeatureMoroccancul-ezgif com-webp-to-jpg-converter](https://github.com/Tensor-Titans/Lmaghrib-BinYedik/assets/49345542/5ee03377-1f54-4fac-bb4e-1a252fec07d9)

 
 # This project was made in the 2024 ThinkAI GenAI Hackathon Under the theme of Tourism 
 
 
 Lmaghrib-BinYedik Combines detailed information on Moroccan monuments, directions, pricing, and assistance into a single, user-friendly chatbot like platform.

 ## We Offer:

- **Comprehensive Information**: Detailed descriptions and histories of Moroccan monuments.
- **Navigation Assistance**: Accurate directions and maps to help you explore the city you visied with ease.
- **Pricing Details**: Up-to-date information on Monuments entry fees, food prices, and other costs.
- **User Support**: Assistance and tips to enhance your travel experience.


## Prerequisites

- Python 3.12.0


## Approach

The Project was divided into tasks in which we tried different techniques.

### Task 1 : Monument Identification

| Model     | Accuracy                          | Flexibility |  Chosen | 
|-----------|-----------------------------------|-----------|------| 
| YoloV8 Classification     | High| Low (limited number of classes) |❌ |
| Bing Reverse Search | Average     | Average (doesn't work too well with new data) |❌ |
| Google Lens      | High              | High   |✅|



Based on these results we tempted for using the Google Lens API to conduct online searches for images corresponding to the input image, specifically focusing on monuments in Morocco. This process allowed us to gather a diverse set of images related to the given monument.
We then utilized the LLM, LLaMA3, to process and analyze the associated image data such as title, enabling it to pinpoint the exact name of the monument depicted.
We chose LLaMA3 since it's a free and open source , we chose the 8 billion parameters model, because it's fast in inference and its performance is good enough for our use case.






### Task 2 : Information Retriever
With the monument’s name identified, LLaMA3 serves a dual role. It also acts as an interactive tool to answer and elaborate on queries about the monument, providing users with detailed, accessible explanations and enhancing their overall understanding.
Further, we employ LangGraph to orchestrate and manage the interaction flows within our application. LangGraph facilitates the creation of complex, stateful interaction chains, which are essential for maintaining context and continuity in conversations with users.

| Technique   | Accuracy                       | Speed    | Relevancy | Chosen |
|-----------|-----------------------------------|-----------|--------|--------|
| Llama3 Knowledge     | High| Fast (doesn't need extra steps to get data) | Low  |❌ |
| WebSearch | High     | Slow  | High|✅ |

Based on the data retrieved we format it into a suitable format that we can display into the GUI as a markdown with interactive links.

### Task 3 : Scam prevention for tourists

While scouring the internet, to look for problems that tourist may encouter, we found the greatest one by a great deal at that too, was the fact that some tourists get scammed, by overpaying on certain necessary items, so we scraped the Marjane Catalogs to build our food prices dataset
| Technique   | Accuracy                       | Speed    | Relevancy | Dependant on Dataset | Chosen |
|-----------|-----------------------------------|-----------|--------|--------|--------|
| Llama3 Knowledge     | Medium| Fast (doesn't need extra steps to get data) | Low  |No |❌ |
| Llama3 Prompt Engineered  | High(But can only take a small subset of dataset) | Slow (It uses up token for taking the data as context) | High  |Yes |❌ |
| WebSearch | High     | Slow  | High |No |✅ |
| Gemini FineTuned | High     | Average | Medium  |Yes |✅ |
| CsvAgent | Medium     |Fast  | Low (Needs Exact Name ) |Yes |❌ |




## Extra Tasks :

#### History Persistence
#### Context relevancy in conversation
#### On_Chat_Resume
#### Authentification mechanism
#### Multiple Model profiles
#### 
![gpt4](https://github.com/Tensor-Titans/Lmaghrib-BinYedik/assets/77627747/ee42892b-9ee8-46c9-9203-33c8439184b0)




![identify our historical monuments](https://github.com/Tensor-Titans/Lmaghrib-BinYedik/assets/77627747/450391c4-8fd3-4d6c-b86a-dcb340880eba)

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
  

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

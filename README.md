# Lmaghrib-BinYedik
![DALLE2024-05-1818 45 51-AbannerforaGitHubrepositoryforanapplicationcalledLmaghrib-BinYedikwhichguidestouristsinMorocco ThedesignshouldfeatureMoroccancul-ezgif com-webp-to-jpg-converter](https://github.com/Tensor-Titans/Lmaghrib-BinYedik/assets/49345542/5ee03377-1f54-4fac-bb4e-1a252fec07d9)

 Lmaghrib-BinYedik Combines detailed information on Moroccan monuments, cuisine, directions, pricing, and assistance into a single, user-friendly chatbot like platform.

 ## We Offer:

- **Comprehensive Information**: Detailed descriptions and histories of Moroccan monuments.
- **Culinary Insights**: Information about traditional Moroccan cuisine, including popular dishes and recipes.
- **Navigation Assistance**: Accurate directions and maps to help you explore the city you visied with ease.
- **Pricing Details**: Up-to-date information on Monuments entry fees, food prices, and other costs.
- **User Support**: Assistance and tips to enhance your travel experience.


## Prerequisites

- Python 3.12.0


## Approach

<img src="https://seeklogo.com/images/G/google-lens-logo-0F69C74B83-seeklogo.com.png" width="75" height="75" alt="Google Lens">

Our solution leverages the Google Lens API to perform searches for images related to an input image, focusing specifically on Moroccan monuments. 
This approach allows us to gather a broad range of related images.

We then utilize the LLM, LLaMA3, to process and analyze the associated image data, enabling it to pinpoint the exact name of the monument depicted.

With the monument’s name identified, LLaMA3 serves a dual role. It acts as an interactive tool to answer and elaborate on queries about the monument, providing users with detailed, accessible explanations and enhancing their overall understanding.



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

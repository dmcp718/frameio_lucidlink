import os
from fastapi import FastAPI, HTTPException, Request
import httpx
import aiofiles
from pathlib import Path
import logging
import uvicorn

# Setup basic logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

bearer_token = os.getenv('BEARER_TOKEN')
save_path = os.getenv('SAVE_PATH')

# Define the download function
async def download_and_save_data(pre_signed_url, output_directory, output_file_name):
    try:
        # Fetch data from the pre-signed URL
        async with httpx.AsyncClient() as client:
            response = await client.get(pre_signed_url)
            downloaded_data = response.content  # Gets the response content as bytes

        # Ensure the output directory exists
        Path(output_directory).mkdir(parents=True, exist_ok=True)

        # Construct the full output file path
        output_file_path = Path(output_directory) / output_file_name

        # Save the data to the desired location asynchronously
        async with aiofiles.open(output_file_path, 'wb') as f:
            await f.write(downloaded_data)

        logging.info(f"'{output_file_name}' downloaded and saved successfully.")
    except Exception as e:
        logging.error(f'Error downloading and saving data: {e}')
        # Optionally, re-raise the exception if you want to handle it further up the call stack
        # raise e

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        # logging.info("Received webhook request")
        
        body = await request.json()
        # Access the asset_id from the nested resource dictionary
        asset_id = body.get("resource", {}).get("id")
        if not asset_id:
            raise HTTPException(status_code=400, detail="Asset ID missing in request.")

        # Fetch asset details
        async with httpx.AsyncClient() as client:
            params = {"include_deleted": "true", "type": "file"}
            headers = {"Authorization": f"Bearer {bearer_token}"}
            response = await client.get(f"https://api.frame.io/v2/assets/{asset_id}", params=params, headers=headers)
            
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to retrieve asset details.")

            data = response.json()
            asset_name = data['name']
            creator_name = data['creator']['name']
            project_name = data['project']['name']
            pre_signed_url = data['original']

            # Call the download function with the correct parameters
            await download_and_save_data(pre_signed_url, Path(save_path) / project_name / creator_name, asset_name)

        return {"message": "Webhook processed and data downloaded successfully."}
    except Exception as e:
        logging.error(f"Error processing webhook request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

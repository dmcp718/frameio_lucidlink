 frameio_lucidlink webhook app
 ------------------------------------------------------------------
 AUTHOR: [LucidLink Solutions]
 NAME: frameio_lucidlink
 DESCRIPTION: GUI app to configure and operate webhook connector


 THE SCRIPT IS PROVIDED “AS IS” AND “AS AVAILABLE” AND IS WITHOUT
 WARRANTY OF ANY KIND. PLEASE REVIEW ALL TERMS AND CONDITIONS.
 https://www.lucidlink.com/legal-documents
 ------------------------------------------------------------------


This app configures a host system to create an ngrok tunnel and frame.io webhook listener. As the app receives webhooks from frame.io, the app initiates a download of the asset from frame.io to the designated LucidLink Filespace directory.

Unzip the project directory in your chosen location. To setup the app on a host system for the first time, open Terminal and run these commands:

```
cd path/to/directory-where-you-unzipped-file
sudo chmod +x setup_script.command
sudo chmod +x run_app.command
./setup_script.command
```

Once the initial setup completes, run these commands:

```
source venv/bin/activate
./run_app.command
```

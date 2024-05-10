# frameio_lucidlink webhook app

This app configures a host system to create an ngrok tunnel and frame.io webhook listener. As the app receives webhooks from frame.io, the app initiates a download of the asset from frame.io to the designated LucidLink Filespace directory.

Unzip the project directory in your chosen location. To setup the app on a host system for the first time, open Terminal and run these commands:

```
cd path/to/directory-where-you-unzipped-file
sudo chmod +x setup_script.command
./setup_script.command
```

Once the initial setup completes, run these commands:

```
source venv/bin/activate
./run_app.command
```

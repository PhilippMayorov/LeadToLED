# Welcome to the leadtoLED Project 🌟

Ever found yourself scrambling to jot down notes before the whiteboard is wiped clean? 📚🖊️ Say goodbye to those days! Introducing **leadtoLED**—the innovative pen attachment that tracks every swoosh and stroke of your writing and magically beams your notes online. Get ready to capture every word with flair and precision!

## Ignite Your leadtoLED Adventure! 🔥

Ready to transform your note-taking experience? Just follow these simple steps:

1. Fire up your terminal and run: `pip install -r requirements.txt`
2. Infuse the power of MongoDB and Solace with your ENV data—secret ingredients for your success!
3. Launch the visual spectacle: `python Canvas.py`

## Discover the Magic Inside the Box! 🎩🐇

Here's a peek at the treasures you'll find in this project:

- **Hardware/**: The heartbeat of our innovation.
  - **final/**
    - `accelerometer.ino`: Our Arduino wizardry for accelerometer data finesse.
    - `positiontracker.py`: The Python spell for tracing your magical movements.
- **main/**: The realm of core enchantments.
  - **backend/**: The alchemy lab where data dances and transforms.
    - `getCoords.py`: Summon coordinates from the ether.
    - `seedDB.py`: Sprinkle the seeds of data into MongoDB.
    - `mongodb_handler.py`: Conjure and converse with MongoDB entities.
    - `mqtt_handler.py`: Weave the MQTT messaging magic.
    - `plotter.py`: Paint data into visual poetry.
  - **frontend/**: The stage where your creations come to life.
    - `accel_to_draw.py`: Translate accelerometer gestures into digital masterpieces.
    - `Canvas.py`: The simple canvas where your first sketches take shape.
    - `Canvas2.py`: An advanced canvas for complex and colorful expressions.
    - `displayCanvas.py`: Showcase your artistry for the world to see.
    - `main.py`: The grand gateway to your frontend fortress.
  - `plot_test.py`: Test the limits of your plotting prowess.
  - `tracking_server.py`: The diligent server that never sleeps, keeping track of your data.
- **.env**: Your secret vault for sensitive spells (keep it safe from prying eyes!).
- **.gitignore**: The cloak of invisibility for your files.
- **acc_sim.py**: Simulate the sways and swerves of your accelerometer.
- **config.properties**: The rulebook that governs the behavior of your project.
- **config.properties.template**: A parchment to guide your configuration setup.
- **README.md**: The scroll that tells the tale of your project.
- **requirements.txt**: The list of potions needed for your project to thrive.

## Challenges We Embraced Along the Way 🚀

- Unraveling the mysteries of getting Solace to sync with our accelerometer—a true adventure!
- Our accelerometer was shy at first—it didn't want to talk to Solace, but we had a heart-to-heart.
- Translating the dynamic dance of 3D hand movements into precise digital traces on your screen. What a journey!

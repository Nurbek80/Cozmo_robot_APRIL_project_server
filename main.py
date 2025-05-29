import pycozmo
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import time

app = FastAPI()

cli = pycozmo.Client()


@app.on_event("startup")
def startup_event():
    cli.start()
    time.sleep(2)  # give USB interface time
    cli.connect()
    cli.anim_controller.enabled = True
    cli.enable_animations()

    # 👇 Load animations after enabling them
    cli.load_anims()

    print("✅ Cozmo connected and animations loaded!")
    #print(cli.anim_names)


@app.on_event("shutdown")
def shutdown_event():
    cli.disconnect()
    cli.stop()
    print("🛑 Cozmo disconnected.")


class Command(BaseModel):
    command: str


@app.post("/command")
def handle_command(cmd: Command):
    command = cmd.command
    print(f"📥 Received command: {command}")

    if command == "forward":
        cli.drive_wheels(50, 50, duration=5.0)
        return {"status": "Moved forward"}
    elif command == "backward":
        cli.drive_wheels(-50, -50, duration=5.0)
        return {"status": "Moved backward"}
    elif command == "turn_left":
        cli.drive_wheels(-50, 50, duration=4.0)
        return {"status": "Turned left"}
    elif command == "turn_right":
        cli.drive_wheels(50, -50, duration=4.0)
        return {"status": "Turned right"}
    elif command == "stop":
        cli.drive_wheels(0, 0)
        return {"status": "Stopped"}
    elif command == "light_on":
        cli.set_backpack_lights(
            pycozmo.lights.green_light,
            pycozmo.lights.green_light,
            pycozmo.lights.green_light,
            pycozmo.lights.green_light,
            pycozmo.lights.green_light
        )
        return {"status": "Lights on"}

    elif command == "light_off":
        cli.set_backpack_lights(
            pycozmo.lights.off_light, pycozmo.lights.off_light,
            pycozmo.lights.off_light, pycozmo.lights.off_light,
            pycozmo.lights.off_light
        )
        return {"status": "Lights off"}

    # 🔥 Анимации
    elif command == "anim_happy":
        cli.play_anim(name="anim_greeting_happy_03")
        return {"status": "Played happy animation"}
    elif command == "anim_angry":
        cli.play_anim(name="anim_explorer_drvback_loop_01")
        return {"status": "Played angry animation"}
    elif command == "anim_look":
        cli.play_anim(name="anim_explorer_idle_02_head_angle_20")
        return {"status": "Played look around animation"}

    return {"status": f"Unknown command: {command}"}


# 📂 Раздача фронтенда
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

@app.get("/tutorial")
def serve_tutorial():
    return FileResponse("static/tutorial.html")


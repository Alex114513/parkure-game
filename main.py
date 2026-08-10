import tools
import const
import platform
import scenes.main_title as main_title

if __name__ == "__main__":
    tools.log(f"game start,debug enabled:{const.debug_mode}" , const.INFO)
    tools.log("System Information:" , const.DEBUG)
    tools.log(f"    System platform: {platform.system()}" , const.DEBUG)
    tools.log(f"    machine architecture: {platform.machine()}" , const.DEBUG)
    tools.log(f"    python version: {platform.python_version()}" , const.DEBUG)
    tools.log(f"    Hardware: CPU: {platform.processor()}" , const.DEBUG)
    main_title.start()
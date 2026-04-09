import tools
import const
import scenes.main_title as main_title

if __name__ == "__main__":
    tools.log(f"game start,debug enabled:{const.debug_mode}" , const.INFO)
    main_title.start()
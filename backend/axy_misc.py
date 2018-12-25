import yaml
import os

def load_configuration(app_yaml_location: str) -> bool:
    """Function that loads axy application configuration from app.yaml

    Enviroment variable created for each param in env_variables section of app.yaml

    Args:
        app_yaml_location (str): Path to app.yaml location.

    Returns:
        bool: The return value. True for success.
        
    Examples:
        Access configuration variables like os.environ['AXY_VERSION']

    Raises:
        FileNotFoundError: Cant find app.yaml
        ValueError: Cant parse app.yaml
        LookupError: No env_variables section in app.yaml
    """    
    app_yaml = os.path.join(app_yaml_location, '', 'app.yaml')
    if os.path.isfile(app_yaml) is False:
        raise FileNotFoundError('Configuration failed, app.yaml not found')
            
    if os.getenv("SERVER_SOFTWARE", "").startswith("Google App Engine") is False:
        with open(app_yaml, 'r') as stream:
            try:
                yaml_vars = yaml.safe_load(stream)
                if 'env_variables' not in yaml_vars:
                    raise LookupError("Configuration failed, no env_variables in app.yaml")
                for key, value in yaml_vars['env_variables'].items():
                    os.environ[key] = value
            except yaml.YAMLError as exc:
                raise ValueError("Configuration failed, cant parse yaml - " + exc)
    return True
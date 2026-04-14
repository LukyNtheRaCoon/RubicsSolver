# Falešný modul copy pro MicroPython

def copy(obj):
    """Mělká kopie objektu."""
    if isinstance(obj, list):
        return obj[:]
    elif isinstance(obj, dict):
        res = {}
        for k, v in obj.items():
            res[k] = v
        return res
    elif hasattr(obj, '__class__'):
        # Zkusíme vytvořit novou instanci třídy (např. pro CubieCube)
        try:
            new_obj = obj.__class__()
            if hasattr(obj, '__dict__'):
                for k, v in obj.__dict__.items():
                    if isinstance(v, list):
                        setattr(new_obj, k, v[:])
                    else:
                        setattr(new_obj, k, v)
            return new_obj
        except Exception:
            pass
    return obj

def deepcopy(obj, memo=None):
    """Hluboká kopie objektu."""
    if isinstance(obj, list):
        return [deepcopy(item) for item in obj]
    elif isinstance(obj, dict):
        res = {}
        for k, v in obj.items():
            res[k] = deepcopy(v)
        return res
    elif hasattr(obj, '__class__'):
        try:
            new_obj = obj.__class__()
            if hasattr(obj, '__dict__'):
                for k, v in obj.__dict__.items():
                    setattr(new_obj, k, deepcopy(v))
            return new_obj
        except Exception:
            pass
    return obj
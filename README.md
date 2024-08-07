# Description

A python library for utilizing Google Authentication for Streamlit Applications.

## Installation

pip install git+https://github.com/edire/streamlit-authentication.git

## Example

```python
import os
from streamlit_authentication.google_oauth import authenticate

os.environ['AUTHORIZED_USERS'] = '*@gmail.com, eric.dire@direanalytics.com'

@authenticate
def main():
    st.write('You are successfully authenticated!')

main()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License

## Updates

08/08/2024 - modularized and removing timing delays.<br>
08/02/2024 - added cryptography to install list.<br>
06/24/2024 - Initial Commit.
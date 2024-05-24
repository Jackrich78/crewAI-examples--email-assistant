#  added 3 lines to try and ignore depgraction warnings
import warnings
from langchain._api import LangChainDeprecationWarning
warnings.simplefilter("ignore", category=LangChainDeprecationWarning)


from src.graph import WorkFlow

app = WorkFlow().app
app.invoke({})
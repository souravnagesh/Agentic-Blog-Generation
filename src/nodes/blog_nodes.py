from src.states.blogstate import BlogState, Blog
from langchain_core.messages import HumanMessage

class BlogNode:
    def __init__(self,llm):
        self.llm= llm
    
    def title_creation(self, state:BlogState):
        """
        To create a Blog title from the topic
        """

        if "topic" in state and state["topic"]:
            prompt="""
                    You are a expert blog content writer. Use Markdown formatting and generate 
                    a blog title for the given topic:{topic}. The title should be creative and
                    SEO friendly
                    """
            
            system_message= prompt.format(topic=state["topic"])
            response= self.llm.invoke(system_message)
            return {"blog":{"title": response.content}}
    
    def content_generation(self, state:BlogState):
        """
        Node to generate the blog content
        """
        if "topic" in state and state["topic"]:
            prompt= """
                    You are expert blog writer. Use Markdown formatting.
                    Generate a detailed blog content with detailed breakdown for the topic:{topic}
                    """
            system_message= prompt.format(topic=state["topic"])
            response= self.llm.invoke(system_message)
            return{"blog":{"title": state["blog"]["title"], "content": response.content}}
        
    def translation(self, state:BlogState):
        """
        Translate the content to the specified language
        """

        translate_prompt="""
            Translate the following content into {current_language}.
            - Maintain the original tone, styling and formatting.
            - Adapt cultural refereneces and idioms to be appropriate for {current_language}.

            ORIGINAL CONTENT:
            {blog_content}
            """
        
        blog_content= state["blog"]["content"]
        message=[
            HumanMessage(translate_prompt.format(current_language=state["current_language"], blog_content=blog_content))
        ]

        translated_content= self.llm.with_structured_output(Blog).invoke(message)
        return {"blog":{"title": translated_content.title, "content":translated_content.content}}
    
    def route(self, state:BlogState):
        return {"current_language": state["current_language"]}
    
    def route_decision(self, state:BlogState):

        if state["current_language"]== "kannada":
            return "kannada"
        elif state["current_language"] == "japanese":
            return "japanese"
        else:
            return state["current_language"]
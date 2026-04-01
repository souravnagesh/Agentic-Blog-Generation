from src.states.blogstate import BlogState

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
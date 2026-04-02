from langgraph.graph import StateGraph, START, END
from src.llms.openaillm import OpenAILLM
from src.states.blogstate import BlogState
from src.nodes.blog_nodes import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm= llm
        self.graph= StateGraph(BlogState)
    
    def build_topic_graph(self):
        """
        Build a graph to generate a blog based on topic
        """

        self.blog_node_obj= BlogNode(self.llm)

        self.graph.add_node("title_creation",self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation",self.blog_node_obj.content_generation)

        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation","content_generation")
        self.graph.add_edge("content_generation", END)

        return self.graph
    
    def build_language_graph(self):
        """
        Build a graph for blog generation with inputs topic and language
        """

        self.blog_node_obj= BlogNode(self.llm)

        self.graph.add_node("title_creation",self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation",self.blog_node_obj.content_generation)
        self.graph.add_node("route",self.blog_node_obj.route)
        self.graph.add_node("Kannada_translation",lambda state: self.blog_node_obj.translation({**state, "current_language":"kannada"}))
        self.graph.add_node("Janpanese_translation",lambda state: self.blog_node_obj.translation({**state,"current_language":"japanese"}))

        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation","content_generation")
        self.graph.add_edge("content_generation","route")
        self.graph.add_conditional_edges("route",self.blog_node_obj.route_decision,
                                         {
                                             "kannada":"Kannada_translation",
                                             "japanese":"Janpanese_translation"
                                         })
        self.graph.add_edge("Kannada_translation",END)
        self.graph.add_edge("Janpanese_translation",END)

        return self.graph
    
    def setup_graph(self,usecase):
        if usecase=='topic':
            self.build_topic_graph()
        elif usecase=='language':
            self.build_language_graph()
        
        return self.graph.compile()
    

## Below code is for langsmith langgraph studio

llm= OpenAILLM().get_llm()

graph_builder= GraphBuilder(llm)
graph= graph_builder.build_topic_graph().compile()
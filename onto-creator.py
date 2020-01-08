""" Creating c_schema ontology from scratch with code using owlready2.
 Manual: https://owlready2.readthedocs.io/en/latest """

from owlready2 import *

my_iri = 'http://vstu.ru/poas/se/c_schema_2020-01'

c_schema = get_ontology(my_iri)






with c_schema:


	####################################
	######## General Properties ########
	####################################

	# # >
	# class referencesTo( FunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass  # direct part
	# # >
	# class hasOnePart( FunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass  # direct part
	# # >
	# class hasSibling( FunctionalProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass  # (directed) base for any Next
	# # >
	# class hasOnePartTransitive( TransitiveProperty,  # transitive !
	# 	FunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass  # base for FirstAct
	# # >
	# class hasUniqueData( FunctionalProperty, DataProperty): pass  # datatype property base

	references = [AsymmetricProperty, IrreflexiveProperty]
	referencesToUnique = [FunctionalProperty, AsymmetricProperty, IrreflexiveProperty]
	referencedByUnique = [InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty]
	mutualUnique = [FunctionalProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty]
	hasUniqueData = [FunctionalProperty, DataProperty]


	###############################
	######## Code Classes ########
	###############################

	# >
	class Algorithm(Thing):
		comment = 'Root of an algorithm tree.'
	# >
	class CodeElement(Thing):
		"""docstring for CodeElement"""
		comment = 'Base for Statements & Expresions, etc.'
	# ->
	class Function(CodeElement): pass
	# ->
	class Statement(CodeElement): pass
	# -->
	class Empty_st(Statement): pass
	# -->
	class FuncCall(Statement): pass
	# -->
	class Block(Statement): pass
	# --->
	class ControlFlow(Statement): pass
	# ---->
	class Decision(ControlFlow): pass
	# ----->
	class IF_st(Decision): pass
	# ----->
	# class SWITCH_st(Decision): pass
	# ---->
	class Loop(ControlFlow): pass
	# ----->
	class FOR_st(Loop): pass
	# ----->
	class WHILE_st(Loop): pass
	# ----->
	class DO_st(Loop): pass

	# -->
	class BREAK_st(Statement): pass
	# -->
	class CONTINUE_st(Statement): pass
	# -->
	class RETURN_st(Statement): pass

	# ->
	class Expression(CodeElement): pass





	#################################
	######## Code Properties ########
	#################################

	""" |  In addition, the following subclasses of Property are available: FunctionalProperty, InverseFunctionalProperty, TransitiveProperty, SymmetricProperty, AsymmetricProperty, ReflexiveProperty, IrreflexiveProperty. They should be used in addition to ObjectProperty or DataProperty (or the ‘domain >> range’ syntax)."""

	# ->
	# class hasSubExpr( CodeElement >> Expression , *references): pass
	# -->
	class hasCondition( (Decision | Loop) >> Expression , *referencesToUnique): pass
	class hasFORInit(   FOR_st >> Expression , 			  *referencesToUnique): pass
	class hasFORUpdate( FOR_st >> Expression , 			  *referencesToUnique): pass

	# ->
	class hasSubStmt( CodeElement >> Statement , *references): pass
	# ->
	class hasBody( (Loop | Function) >> Statement , *referencesToUnique): pass
	# ->
	class hasThenBranch( IF_st >> Statement , *referencesToUnique): pass
	class hasElseBranch( IF_st >> Statement , *referencesToUnique): pass

	# ->
	class hasFirstSt( Block >> Statement , *referencesToUnique): pass
	# ->
	class hasLastSt( Block >> Statement , *referencesToUnique): pass
	# ->
	class hasNextSt( Statement >> Statement , *mutualUnique):
		comment = 'Ordering within Block'

	# ->
	class hasFunc( Algorithm >> Function , *references): pass

	# ->
	class hasName( Function >> str , *hasUniqueData): pass
	# ->
	class callOf( FuncCall >> Function , *referencesToUnique): pass

	# ->
	class breaksLoop( BREAK_st >> Loop , 	*referencesToUnique): pass
	# ->
	class continuesLoop( CONTINUE_st >> Loop , *referencesToUnique): pass
	# ->
	class returnsFrom( RETURN_st >> Function , *referencesToUnique): pass





	###############################
	######## Trace Classes ########
	###############################

	# >
	class TraceElement(Thing):
		comment = 'Base for Act & Context trace elements'
	# ->
	class Act(TraceElement): pass  # atomic "Act"
	# -->
	class ConditionAct(Act): pass  # expression Act, evals to True or False

	# ->
	class Context(TraceElement): pass
	# -->
	class BlockContext(Context): pass
	# -->
	class DecisionContext(Context): pass
	# --->
	class IF_Context(DecisionContext): pass
	# -->
	class LoopContext(Context): pass
	# --->
	class WHILE_Context(LoopContext): pass
	# --->
	class FOR_Context(LoopContext): pass
	# --->
	class DO_Context(LoopContext): pass



	##################################
	######## Trace Properties ########
	##################################

	# # >
	# class hasFirstAct( Context >> Act , hasOnePartTransitive): pass  # over hasFirst(c, a) & Act(a)
	# # >
	# class hasLastAct( Context >> Act , hasOnePartTransitive): pass  # over hasLast(c, a) & Act(a)
	# # ->
	# class hasFirst( Context >> TraceElement , hasOnePart): pass
	# # ->
	# class hasLast( Context >> TraceElement , hasOnePart): pass


	# # >
	# class hasNextAct( Act >> Act , hasSibling): pass
	# # ->
	# class hasNext( Context >> TraceElement , hasSibling): pass  # (hasNextL - on same nesting Level)
	# # ->
	# class before( Context >> TraceElement , hasOnePartTransitive): pass  # over hasNextL

	# # ->
	# class hasOrigin( TraceElement >> CodeElement , referencesTo): pass

	# # >
	# class evalsTo( ConditionAct >> bool , DataProperty): pass





	##############################
	######## Rule Classes ########
	##############################

	# >
	class GenericRule(Thing):
		comment = 'Base for all rules'
        # name
	# ->
	class TraceRule(GenericRule):
		comment = 'Base for all trace rules'


	# -->
	class SequenceRule(TraceRule): pass
	# --->
	class StartActBeforeEndActRule(SequenceRule): pass
	# ---->
	class ActIsContainedInSequenceRule(SequenceRule): pass
	# ---->
	class OnlyOneActExcecutionInSequenceRule(SequenceRule): pass
	# ---->
	class ExecuteActABeforeActBInSequenceRule(SequenceRule): pass

	# -->
	class AlternativeRule(TraceRule): pass
	# --->
	class AlternativeActExecuteRule(AlternativeRule): pass

	# -->
	class LoopRule(TraceRule): pass
	# --->
	class ExecuteBodyActAfterFalseConditionActRule(LoopRule): pass

    # --->
	class WHILE_Rule(LoopRule): pass
	# ---->
	class WhileLoopBodyActExecuteRule(WHILE_Rule): pass



	#################################
	######## Rule Properties ########
	#################################

	# >
	class description( GenericRule >> str , DataProperty, FunctionalProperty): pass



	###############################
	######## Error Classes ########
	###############################

	# >
	class GenericError(Thing):
		comment = 'Base for all errors'
	# ->
	# class Act(TraceElement): pass  # atomic "Act"


	##################################
	######## Error Properties ########
	##################################





	############################
	######## SWRL Rules ########
	############################

	rules = {
# 		"BeforeActTransitive": """ Act(?b) ^ Act(?c) ^ c_schema:Act(?a) ^ beforeAct(?a, ?b) ^ beforeAct(?b, ?c) -> beforeAct(?a, ?c) """ ,
		"NextL_to_before": """ hasNext(?a, ?b) -> beforeAct(?a, ?b) """ ,

# 		"NextL_to_before": """
#         """ ,
	}


def upload_rdf_to_SPARQL_endpoint(graphStore_url, rdf_file_path):
	import requests
	with open(rdf_file_path, 'rb') as f:
		r = requests.post(
		    graphStore_url,  # ex. 'http://localhost:3030/my_dataset/data',
		    files={'file': ('onto.rdf', f, 'rdf/xml')}
		)

	if r.status_code != 200:
		print('\nError uploading file! HTTP response code: %d\nReason: %s\n' % (r.status_code, r.reason))
		return False
	else:
		print('Uploading file successful.')
		return True


def main():

	############################
	######## Export RDF ########
	############################

	# onto_name = c_schema.base_iri.split('/')[-1]  # adds '#' at end
	onto_name = my_iri.split('/')[-1]
	rdf_filename = onto_name + '.rdf'

	c_schema.save(file=rdf_filename, format='rdfxml')
	print("Saved RDF file: {} !".format(rdf_filename))

	# upload_rdf_to_SPARQL_endpoint('http://localhost:3030/c_owl/data', rdf_filename)



if __name__ == '__main__':
	main()
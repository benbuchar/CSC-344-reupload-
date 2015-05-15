/**
 * Created by Ben on 4/8/2015.
 **/
object Main {
    abstract class Expression

      case class And(e1: Expression, e2: Expression) extends Expression
      case class Or(e1: Expression, e2: Expression) extends Expression
      case class Not(e: Expression) extends Expression
      case class Var(v: String) extends Expression
      case class Const(b: Boolean) extends Expression

      var norm : String = ""
      type Environment = String => Boolean

      def eval(exp: Expression, env: Environment): Boolean = exp match {
        case And(e1, e2) => eval(e1, env) && eval(e2, env)
        case Or(e1, e2)  => eval(e1, env) || eval(e2, env)
        case Not(e)      => !eval(e, env)
        case Var(v)      => env(v)
        case Const(b)    => b
      }
      /**
      def evalToNormal(exp: Expression, env: Environment): Expression = exp match{
        //case And(e1, Or(e2, e3)) => "(%s and %s) or (%s and %s)".format(evalToNormal(e1, env), evalToNormal(e2, env), evalToNormal(e1, env), evalToNormal(e3, env))
        case And(Or(e2, e3), e1) => "(%s and %s) or (%s and %s)".format(evalToNormal(e1, env), evalToNormal(e2, env), evalToNormal(e1, env), evalToNormal(e3, env))
        case Or(And(e1, e2), e3) => "(%s or %s) and (%s or %s)".format(evalToNormal(e1, env), evalToNormal(e2, env), evalToNormal(e3, env))
        case Or(e3,(And(e1, e2)))=> "(%s or %s) and (%s or %s)".format(evalToNormal(e1, env), evalToNormal(e2, env), evalToNormal(e3, env))
        case Not(Or(e1, e2))     => "(!%s or %s)".format(evalToNormal(e1,env), evalToNormal(e2,env))
        case Not(And(e1, e2))    => "(!%s and !%s)".format(evalToNormal(e1, env), evalToNormal(e2,env))
        case Not(Or(e1, Not(e2)))=> "(!%s and !%s)".format(evalToNormal(e1, env), evalToNormal(e2, env))
        case Not(Var(e))         => eval(Not(Var(e)), env).asInstanceOf[String]
        case Const(e)            => e.asInstanceOf[String]
        case Var(e)              => e
        case And(_, Or(e2, e3))    => evalToNormal(_, env)  and evalToNormal(e2, env)
      }**/
      def evalToNormal(exp: Expression, env: Environment, norm: String): String = exp match{
        case Or(And(e1, e2), e3) => norm.concat(evalToNormal(Or(e1, e3), env, norm) + evalToNormal(Or(e2, e3), env, norm))
        case Or(e1, And(e2, e3)) => norm.concat(evalToNormal(Or(e1, e2), env, norm) + evalToNormal(Or(e1, e3), env, norm))
        case And(e1, Or(e2, e3)) => norm.concat(evalToNormal(Or(e1, e2), env, norm) + evalToNormal(Or(e1, e3), env, norm) + " ")
        case And(e1, Not(Or(e2, e3))) => norm.concat("(" + evalToNormal(e1, env, norm) + ") " +evalToNormal(And(Not(e2), Not(e3)), env, norm))
        case Or(e1, Not(And(e2, e3))) => norm.concat(evalToNormal(Or(e1, Not(e2)), env, norm) + evalToNormal(Or(e1, Not(e3)), env, norm) + " ")
        case And(e1, e2)         => norm.concat("("+ evalToNormal(e1, env, norm) + ") (" + evalToNormal(e2, env, norm) + ")")
        case Or(e1, e2)          => norm.concat("("+evalToNormal(e1, env, norm) + " or "+ evalToNormal(e2, env, norm)+")")
        case Not(Or(e1, e2))     => norm.concat("(" + evalToNormal(Not(e1), env, norm) + ") (" + evalToNormal(Not(e2), env, norm) + ")")
        case Not(e)              => "¬" + evalToNormal(e, env, norm)
        case Var(e)              => e
        case Const(b)            => ""+b
      }



      def main(args: Array[String]): Unit = {
        val exp1: Expression = And(Var("x"),(Or (Var("x"),(And(Var("y"),(Not(Var("z"))))))))
        val exp2: Expression = And(And(Var("z"),Const(false)),Or(Var("x"), Const(true)))
        val exp3: Expression = Or(Const(true),(Var("x")))
        val exp4: Expression = Not(Var("x"))
        val exp5: Expression = And(Var("x"), Not((Or(Var("x"), Var("y")))))
        val exp6: Expression = Or(Var("x"), Not(And(Var("y"), Var("z"))))
        val expressions = Array(exp1, exp2, exp3, exp4, exp5, exp6)

        println("Expression 1: " + exp1)
        println("Expression 2: " + exp2)
        println("Expression 3: " + exp3)
        println("Expression 4: " + exp4)
        println("Expression 5: " + exp5)
        println("Expression 6: " + exp6)
        println("Choose your binding for x: ")
        val b1 = scala.io.StdIn.readBoolean()
        println("Choose your binding for y: ")
        val b2 = scala.io.StdIn.readBoolean()
        println("Choose your binding for z:")
        val b3 = scala.io.StdIn.readBoolean()

        val env: Environment = {
            case "x" => b1
            case "y" => b2
            case "z" => b3
        }
        var i = 0;
        do {
          println("Choose your expression: ")
          val choice = scala.io.StdIn.readInt()
          println("Evaluation with x=" + b1 + ", y=" + b2 + ", z=" + b3 + " expression " + choice + ": " + eval(expressions(choice - 1), env))
          println("Expression " + choice + " in  CNF:" + evalToNormal(expressions(choice - 1), env, norm))
          i = i + 1
        } while (i <= 10)
      }

}

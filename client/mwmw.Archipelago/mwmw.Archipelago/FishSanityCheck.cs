using GDWeave.Godot;
using GDWeave.Godot.Variants;
using GDWeave.Modding;

namespace mwmw.Archipelago;

public class FishSanityCheck : IScriptMod {
    public bool ShouldRun(string path) => path == "res://Scenes/Singletons/playerdata.gdc";

    public IEnumerable<Token> Modify(string path, IEnumerable<Token> tokens) {
        // print("nope i dont have ", q)
        // same anchor GoalCompletion.cs uses - fires after a new (species, quality) is logged
        var newFishWaiter = new MultiTokenWaiter([
            t => t.Type is TokenType.BuiltInFunc,
            t => t.Type is TokenType.ParenthesisOpen,
            t => t is ConstantToken{Value: StringVariant{Value: "nope i dont have "}},
            t => t.Type is TokenType.Comma,
            t => t is IdentifierToken{Name:"q"},
            t => t.Type is TokenType.ParenthesisClose
        ], allowPartialMatch: false);

        foreach (var token in tokens) {
            if (newFishWaiter.Check(token)) {
                // get_node("/root/mwmwArchipelago").scan_fish_sanity()
                yield return token;

                yield return new Token(TokenType.Newline, 2);
                yield return new IdentifierToken("get_node");
                yield return new Token(TokenType.ParenthesisOpen);
                yield return new ConstantToken(new StringVariant("/root/mwmwArchipelago"));
                yield return new Token(TokenType.ParenthesisClose);
                yield return new Token(TokenType.Period);
                yield return new IdentifierToken("scan_fish_sanity");
                yield return new Token(TokenType.ParenthesisOpen);
                yield return new Token(TokenType.ParenthesisClose);

            } else {
                yield return token;
            }
        }
    }
}

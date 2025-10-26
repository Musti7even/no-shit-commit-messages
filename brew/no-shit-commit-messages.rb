class NoShitCommitMessages < Formula
  desc "AI-powered git commit message generator (no more shitty commits)"
  homepage "https://github.com/usearrow/no-shit-commit-messages"
  url "https://github.com/usearrow/no-shit-commit-messages/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "<fill after release>"
  license "MIT"

  depends_on "python@3.11"

  def install
    bin.install "nscm.py" => "nscm"
  end

  def caveats
    <<~EOS
      Add to your shell:
        alias git='nscm'
      Export your key:
        export OPENAI_API_KEY=sk-...
    EOS
  end
end



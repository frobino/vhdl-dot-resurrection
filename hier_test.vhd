library IEEE;
use IEEE.STD_LOGIC_1164.all;

entity MUX2 is
  port (SEL, A, B : in  std_logic;
        F, E, G   : out std_logic
        );
end MUX2;

architecture STRUCTURE of MUX2 is

  component INV
    port (SEL,A : in  std_logic;
          F : out std_logic);
  end component;

  signal SEL_s, A_s, F_s : std_logic;

begin
  G1 : INV port map (SEL => SEL_s, F => F, A => A);
end;

-------------------------------------------------------------------------------
--! @file
--! @brief Test module
--!
--! Implements test module for doxygen
-------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;

library work;
-------------------------------------------------------------------------------
--! Test entity declaration
-------------------------------------------------------------------------------
entity test2_tb is

end test2_tb;

-------------------------------------------------------------------------------
--! Test architecture declaration
-------------------------------------------------------------------------------
architecture behavioral_test2_tb of test2_tb is

  component test2
    port(
      p_Clk : in  std_logic;
      p_Rst : out std_logic
      );
  end component;

  signal p_Clk, p_Rst, o_Out : std_logic;

begin

  test_2_label : test2 port map (
    p_Clk => p_Clk,
    p_Rst => p_Rst);

end behavioral_test2_tb;

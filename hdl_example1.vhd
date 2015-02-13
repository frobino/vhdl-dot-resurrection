-------------------------------------------------------------------------------
--! @file
--! @brief Test module
--!
--! Implements test module for doxygen
-------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;

library work;
-------------------------------------------------------------------------------
--! Test entity declaration
-------------------------------------------------------------------------------
entity test is
  generic
  (
    g_ClkFreqMHz     : real := 50.0
  );
  port
  (
    p_Clk      : in std_logic;
    p_Rst      : in std_logic
  ); 
end test;
      
-------------------------------------------------------------------------------
--! Test architecture declaration
-------------------------------------------------------------------------------
architecture behavioral_test of test is
  signal sig1 : std_logic := '0';
begin

  -----------------------------------------------------------------------------
  --! @brief Process to manage reception of packets
  --! 
  --! Gets 32 bit words from PROC_RX_WORD32 transfers them to the receive
  --! buffer. Manages frame delimiters and other command codes.
  --! 
  --! @param[in]   p_Rst  Active high asynchronous reset
  --! @param[in]   p_Clk  Clock, used on rising edge
  --!
  --! @vhdlflow [PROC_RX_PKT flow]
  -----------------------------------------------------------------------------
  PROC_RX_PKT : process(p_Rst, p_Clk)
  begin
    sig1 <= not sig1;
  end process PROC_RX_PKT;
 
 
end behavioral_test;

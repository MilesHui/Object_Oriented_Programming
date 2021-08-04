from machine import Enigma
from components import Rotor, Plugboard, Reflector, ALPHABET
from unittest.mock import MagicMock, Mock, patch
import datetime
import pytest


"""
This is the init part
"""

@pytest.fixture
def init():
    enigma = Enigma(key='ABC')
    return enigma

def test_key_3():
    with pytest.raises(ValueError) as err:
        Enigma(key='ABCD')
    assert 'Please provide a three letter string as the initial window setting.' in str(err.value)

def test_init_key(init):
    # enigma = Enigma(key='ABC')
    assert 'ABC' == init.key

def test_init_rotor_order(init):
    assert ['I', 'II', 'III'] == init.rotor_order

def test_init_rotor_order_change():
    enigma = Enigma(key='ABC', rotor_order = ['II', 'I', 'III'])
    assert ['II', 'I', 'III'] == enigma.rotor_order


def test_init_set_rotor_order():
    with patch("machine.Enigma.set_rotor_order") as patched_function:
        Enigma(key='ABC')
    assert patched_function.call_count == 1

def test_init_set_rotor_order_called_with():
    with patch("machine.Enigma.set_rotor_order") as patched_function:
        Enigma(key='ABC', rotor_order=['II', 'I', 'III'])
    assert patched_function.assert_called_with(['II', 'I', 'III']) is None


def test_init_reflector(init):
    assert (isinstance(init.reflector, Reflector)) == True


def test_init_plug(init):
    assert (isinstance(init.plugboard, Plugboard)) == True
    # with patch("components.Plugboard") as patched_function:
    #     Enigma(key='ABC')
    # assert patched_function.call_count == 1


"""
repr part
"""

def test_repr(init):
    x = init.__repr__()
    assert x == 'Keyboard <-> Plugboard <->  Rotor I <-> Rotor  II <-> Rotor  III <-> Reflector \nKey:  + ABC'

"""
encipher part
"""
def test_enipher_called(init):
    init.encipher = Mock()
    init.encipher('hello')
    assert init.encipher.call_count == 1
    assert init.encipher.assert_called_with('hello') is None

def test_encipher_raise(init):
    with pytest.raises(ValueError) as err:
        init.encipher('1')
    assert 'Please provide a string containing only the characters a-zA-Z and spaces.' in str(err.value)

def test_encipher_not_raise(init):
    init.encipher('k')


def test_encipher_condition1(init):
    result = init.encipher('hello')
    assert result == 'ROMUL'

def test_encipher_condition2(init):
    result = init.encipher('HELLO')
    # print(result)
    assert result == 'ROMUL'


def test_encipher_condition3(init):
    result = init.encipher(' HELLO')
    # print(result)
    assert result == 'ROMUL'

def test_encipher_condition4(init):
    result = init.encipher(' HELLO ')
    # print(result)
    assert result == 'ROMUL'

def test_encipher_condition5(init):
    result = init.encipher(' HE  LLO ')
    assert result == 'ROMUL'


def test_encipher_encode_decode_letter_called(init):
    with patch("machine.Enigma.encode_decode_letter") as patched_function:
        message = '    he llo'
        result = init.encipher(message)
    assert patched_function.call_count ==  len(message.upper().replace(" ", "").strip())


def test_encipher_other_rotor():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'])
    result = enigma.encipher(' HELLO ')
    # print(result)
    assert result == 'BJMWJ'

def test_encipher_other_swap():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'], swaps=[('A', 'B')])
    result = enigma.encipher(' HELLO ')
    assert result == 'AJMWJ'



"""
decipher part
"""
def test_decipher_called(init):
    init.decipher = Mock()
    init.decipher('hello')
    assert init.decipher.call_count == 1

def test_decipher_called_encoder(init):
    init.encipher = Mock()
    init.decipher('hello')
    assert init.encipher.call_count == 1
    assert init.encipher.assert_called_with('hello') is None

"""
set_rotor_position part
"""
def test_set_rotor_position__len_not_3(capsys):
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'], swaps=[('A', 'B')])
    enigma.set_rotor_position('AAAA')
    out, err = capsys.readouterr()
    assert "Please provide a three letter position key such as AAA." in out

def test_set_rotor_position_type_not_str(capsys):
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'], swaps=[('A', 'B')])
    enigma.set_rotor_position(123)
    out, err = capsys.readouterr()
    assert "Please provide a three letter position key such as AAA." in out

def test_set_rotor_position_type_not_str_len_not_3(capsys):
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'], swaps=[('A', 'B')])
    enigma.set_rotor_position([1,2,3])
    out, err = capsys.readouterr()
    assert "Please provide a three letter position key such as AAA." in out



def test_set_rotor_position_key():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'], swaps=[('A', 'B')])
    assert enigma.key == 'ABC'
    enigma.set_rotor_position('BAC')
    assert enigma.key == 'BAC'

def test_set_rotor_position_change_setting():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'], swaps=[('A', 'B')])
    with patch("components.Rotor.change_setting") as patched_function:
        enigma.set_rotor_position('BAC')
    # patched_function.assert_called_once_with(['AB', 'CD'], False)
    assert patched_function.call_count == 3
    # patched_function.assert_called_with('C')

def test_set_rotor_position_printIt(capsys):
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'], swaps=[('A', 'B')])
    enigma.set_rotor_position('BAC', printIt=True)
    out, err = capsys.readouterr()
    assert f"Rotor position successfully updated. Now using {enigma.key}." in out


"""
set_rotor_order part
"""
def test_set_rotor_order_init(init):
    assert (isinstance(init.l_rotor, Rotor)) == True
    assert (isinstance(init.m_rotor, Rotor)) == True
    assert (isinstance(init.r_rotor, Rotor)) == True


def test_set_rotor_order_equal(init):
    assert init.m_rotor.prev_rotor == init.r_rotor
    assert init.l_rotor.prev_rotor == init.m_rotor

def test_set_rotor_order_rotor():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'], swaps=[('A', 'B')])
    assert enigma.l_rotor.rotor_num == 'II'
    assert enigma.l_rotor.window == 'A'
    assert enigma.m_rotor.rotor_num == 'I'
    assert enigma.m_rotor.window == 'B'
    assert enigma.m_rotor.next_rotor == enigma.l_rotor
    assert enigma.r_rotor.rotor_num == 'III'
    assert enigma.r_rotor.window == 'C'
    assert enigma.r_rotor.next_rotor == enigma.m_rotor



"""
set_plugs part
"""

def test_set_plugs_swaps(init):
    with patch("components.Plugboard.update_swaps") as patched_function:
        init.set_plugs(['AB', 'CD'])
    patched_function.assert_called_once_with(['AB', 'CD'], False)

def test_set_plugs_swaps_replace(init):
    with patch("components.Plugboard.update_swaps") as patched_function:
        init.set_plugs(['AB', 'CD'],True)
    patched_function.assert_called_once_with(['AB', 'CD'], True)

def test_set_plugs_swaps_printIt(capsys):
    enigma = Enigma(key='ABC')
    enigma.set_plugs(['AB', 'CD'], printIt=True)
    out, err = capsys.readouterr()
    # print(out)
    assert "Plugboard successfully updated. New swaps are:" in out
    assert 'A <-> ' in out
    assert 'C <-> D' in out


def test_set_plugs_swaps_morethan6(capsys):
    enigma = Enigma(key='ABC')
    enigma.set_plugs(['AB', 'CD', 'EF', 'GH', 'IJ', 'KL', 'XY'], True)
    out, err = capsys.readouterr()
    assert "Only a maximum of 6 swaps is allowed." in out



"""
encode_decode_letter part
"""
def test_encode_decode_letter_not_bool():
    enigma = Enigma(key='ABC')
    with pytest.raises(ValueError) as err:
        enigma.encode_decode_letter('*')
    assert 'Please provide a letter in a-zA-Z.' in str(err.value)

def test_encode_decode_letter_in_swap():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'], swaps=[('A', 'B')])
    assert enigma.plugboard.swaps['A'.upper()] == 'B'
    # todo not done

def test_encode_decode_letter_step():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'], swaps=[('A', 'B')])
    with patch("components.Rotor.step") as patched_function:
        enigma.encode_decode_letter('B')
    assert patched_function.call_count == 1


def test_encode_decode_letter_first():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'], swaps=[('A', 'B')])
    x = enigma.encode_decode_letter('B')
    assert x == 'R'




"""
add something not done
"""
def test_not_I_and_V():
    with pytest.raises(ValueError) as err:
        Enigma(key='ABC', rotor_order = ['IIII', 'I', 'III'])
    assert 'Please select I, II, III, or V for your rotor number and provide the initial window setting (i.e. the letter on the wheel initially visible to the operator.' in str(err.value)



def test_Rotor_repr():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'])
    x = enigma.l_rotor.__repr__()
    # print(enigma.l_rotor)
    # out, err = capsys.readouterr()
    # print(x)
    assert "Wiring:" in x
    # assert '{'forward': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'backward': 'AJPCZWRLFBDKOTYUQGENHXMIVS'}' in out
    assert 'Window: A' in x


def test_Reflector_repr():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'])
    x = enigma.reflector.__repr__()
    # print(enigma.l_rotor)
    # out, err = capsys.readouterr()
    # print(x)
    assert 'Reflector wiring:' in x
    assert "{'A': 'Y', 'B': 'R', 'C': 'U', 'D': 'H', 'E': 'Q', 'F': 'S', 'G': 'L', 'H': 'D', 'I': 'P', 'J': 'X', 'K': 'N', 'L'"\
": 'G', 'M': 'O', 'N': 'K', 'O': 'M', 'P': 'I', 'Q': 'E', 'R': 'B', 'S': 'F', 'T': 'Z', 'U': 'C', 'V': 'W', 'W': 'V'"\
", 'X': 'J', 'Y': 'A', 'Z': 'T'}" in x


def test_step_not_enough():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'])
    x = enigma.encipher('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    assert x == 'RYHGFDNZGZNYTYGFRPTTZDZSVXDNNQVIPBMYEXDVNHIFZJFHLKELNMDWZIWWCDEKYLUUKLK'

def test_step_change_very_long():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'])
    string = 'a'
    mul_string = string * 1000
    x = enigma.encipher(mul_string)
    assert x == 'RYHGFDNZGZNYTYGFRPTTZDZSVXDNNQVIPBMYEXDVNHIFZJFHLKELNMDWZIW'\
'WCDEKYLUUKLKPGCUHYUCPBZYSGLHNJQJTWDQLKJWKLSEIJLNOEGWBCYKKYORBEHMYKLZUBJZRUDORLIKEZTDPVGFPZGYGXREEOQPXHKWFCGLKFKTXL'\
'GGIVZCUHJUWQQQTLGKIZTUEIHTXBEFXYWUKVCQWZPOPLMZWBZQCTLKDPTFKQBWZEMTGFUITRNXJFWJHEYWYUHSICVDIYZQTNSCVJFJGNIQEVWEWYVY'\
'CVPKTHLJNVZVQQPBQLVUZYSRFWONQIECDZVSFBESHLGUHBZNEONVXGRHWBPBMTSSEHOFZGHCOMXEOERLFOIWYCXEKQSVPZFDFWILJWIIJECBFZFYGZ'\
'DYGCWFPPDYTXPPSMPTZNOHJJUHZFJWMSJJVBVZDISQTCNNBYHXCSIDHLSDPZCEKPRTXKWOXDMEEWHCJKOIKWMQMOVZRITOWSXWYMOOLYUDHIYWWZMO'\
'GTTMDFEKNHXXXEWMPCKYZXOGQRIDLYRIGRSTGTLSNZGWGDMFHJXSVNCIWXYBNPVKNVKTOSHGTGYHLVOCXCEUKYQDTIMDFLMUSOHBMLRZGCUPSUJDDN'\
'FLIKENTUKCFSPOREMSWDLEBOBXHDKPJGBGRXNVVOHMCDCPUEYRUIVDEPHCBWTGKSVQGMGHZKGRVBUDKQKNJGVIKJRRMBXJRNUNFXIFHMOLDKVTTSBE'\
'JOPMUUCMWNUKRGFOBEEWHCJQTVKCZQZLFOCSSTYCVNLYKXJGIMWGLJDRQCPJWYRSDIVGNDLPNFBOMPQJVDSYJXMLLRPUZPRVNUKXLFNWXRTSTZZWSB'\
'HZSNBVHCCZOIFREMJCSTILBSCUTYYQQCSMGOIVUGCGHTBBOYMXOPKTDCNESYKXJGIFRPBSYRGYRXKMLDKFDSKDIPEFBFBOMHVJJXBLPCCMRYGOYKSV'\
'RNOYCVFYBHDLTPIHMFEDYWPOXLWYW'


def test_step_change_very_long_2():
    enigma = Enigma(key='BAC', swaps=[('A', 'B')], rotor_order=['II', 'I', 'III'])
    string = 'abcdefg  hijklmnopqrstuvwxyz'
    mul_string = string * 30
    x = enigma.encipher(mul_string)
    assert x == "EJNBWBJOWHESSJDVKVXSKUNMZPLAGMMZYPFBJMAJGLZFANVEOAGAUY"\
"GQPWTPXPMORIDAASTZCZNFZWQVPMJPTROBXMJRSWZWXLQNHSOTIINYQTQZUODNEEZEXVFEBNOAGPGRZQPQHGSPYORIGEAFTQPMNEZAKYBMKWSYAB"\
"MMBGEHZSUKIHAHBPCDGKLAKYQQAPKPGHCFZIRTEIDYSPXTCHFEHFRBLBIDIPBBNIBWXOMSDFQGJMDTOZETNVEZMUCGLYLARYLJUWSNFMMJQRELRS"\
"KYKENMZRKDBMBAFJHBAMVGWTZDAFDWMSJKIKGBHYFLHQQPDZBRCOFEHRXYQQZRMUWQIUTHYSSDCJKUKVYAQORHEEUZYDSOJKGDUSEJHLOWXWPHSV"\
"YCIWSKTLQLSICTCNTBZJGFIOHHRIKLTTQRYMDJPSLJRLOGZCKIKOMVPNWPXIGHXSSBYQKZBCCPODGJPITQPTQPCEDGRRVGOTLHPMUIFFPGVXTSUC"\
"ZUFAPBLILJBNJIFZEHLXSSFVYDRUIAOSAALLJDQNOQGTBPNQPHMALXRXROQEBVGOCYDWCSVUUPSOMXFUZACRNLLMMRPMQWRVUEAZSDUIXYGYCYNO"\
"WBMPFSSSNMICYVWKPCZHSSSTMKKEFJWBGGMVQDERAAPBYEAGXWUWOBPHCNHHOINQUYDRLFQMWJNRKERNZAQHAIBDOURKIOUXBXZXGBPBBHBOKXXM"\
"QSHSVUXGITUOONTUTXXMADCSLQLCLLYJDIYTSWBVNRDXVGGZVTUFFF"



def test_step_change_very_long_3():
    enigma = Enigma(key='ZZZ', swaps=[('K', 'L'), ('x', 'y'), ('a', 'Z'), ('n', 'M')], rotor_order=['V', 'I', 'III'])
    string = 'abcdefg  hijklmnopqrstuvwxyz'
    mul_string = string * 30
    x = enigma.encipher(mul_string)
    assert x == "HKHBaIRSFSJIUXXGOAFEDTKHnDGQRJUPSQJaVCBAYNKKCXNIYADJO"\
"VVHIROCUVNTLXFLNIHWTDVKEYLAnCLKFaPKPFnEQRVJXWXnIGDCEXVQVORNQHGKIBUWOVHULHURAKNRJBYVHTBOSDROCDDPaESWQHKEWTEWUEJGa"\
"DXRWPIJKXEBHIaVUTVVGYJTOGVUXaWKIFSHEBTULYNWnHHnFUTSJTDJVAXHLKDIAaGAGaOnNPIPPLQSYTXONGGVCCYDIGBSSRPaVUJQTFUXTYYCT"\
"EaDSHDNBRWQABKCRODBBRYHVJOYnENQKKBJDKaWLRSGnQLnJYIRPSPBDnNQTXGRYRSTEnOAVCBWPIILaLSLRFCQKLKYRYPBVBWHDHAUWHKCFGIGN"\
"VDGaKVIRNRTXnWVUaOTEQWHLDKaCYPInLnLSWTNSYNCCDRIJRUACInCDnIYaCYUWJDXFSNONRaDOALBUKEGIUANaCCAOBUWXXBUDDPNNLSOXLKIC"\
"EDTaXaCSAUYVDQQNELGWKNCQKAQJAYRXAYJnKYaDFVSaGXGFNBNUGPUNQLVIQnJQBWKLLFVYQEENSYEaaFPGCSTRXGINSEWKYQKYRaEFRYCJYUPW"\
"SXOOWDTCVTTSaGEJKVANXBXYLDXRUADCUTBOQRQKQGWDDAHDSVaBWaCKUNEXRDTNEGPYICDOSaDaDBGILHPVWUSaHFaFNBYBaNBWGDHQQDUQKCKC"\
"PFOOVKIOLOAODATATDXILTGTPJCNFJTOIHLXPnTLEJKnKESJAHADNIY"






def test_Rotor_encode_letter_index():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'])
    enigma.r_rotor.encode_letter('A')

def test_Rotor_encode_letter_printIt(capsys):
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'])
    enigma.r_rotor.encode_letter('A', printit=True)
    out, err = capsys.readouterr()
    assert "Rotor III: input = C, output = F" in out

def test_Rotor_encode_letter_return_ALPHABET_output_index(capsys):
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'])
    enigma.r_rotor.encode_letter('A', forward=False, return_letter=True, printit=True)
    out, err = capsys.readouterr()
    # print(out)
    assert "Rotor III: input = C, output = G" in out

def test_update_swaps():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'],swaps=[('K', 'L')])
    assert enigma.plugboard.swaps == {'K': 'L', 'L': 'K'}
    enigma.plugboard.update_swaps(new_swaps=[('K', 'N')])
    assert enigma.plugboard.swaps == {'K': 'N', 'L': 'K', 'N': 'K'}

def test_update_swaps_replace():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'],swaps=[('K', 'L')])
    # print(enigma.plugboard.swaps)
    assert enigma.plugboard.swaps == {'K': 'L', 'L': 'K'}
    enigma.plugboard.update_swaps(new_swaps=[('K', 'N')], replace=True)
    # print(enigma.plugboard.swaps)
    assert enigma.plugboard.swaps == {'K': 'N', 'N': 'K'}

def test_update_swaps_replace():
    enigma = Enigma(key='ABC', rotor_order=['II', 'I', 'III'],swaps=[('K', 'L')])
    # print(enigma.plugboard.swaps)
    assert enigma.plugboard.swaps == {'K': 'L', 'L': 'K'}
    # with pytest.raises() as err:
    enigma.plugboard.update_swaps(new_swaps={('K', 'N')}, replace=True)
    # print(enigma.plugboard.swaps)
    # assert enigma.plugboard.swaps == {'K': 'N', 'N': 'K'}



"""
Randoly do something
"""
def test_1():
    enigma = Enigma(key='ABC', swaps=[('A', 'B'),('C', 'B')], rotor_order=['II', 'I', 'III'])
    x = enigma.encipher('jsksdhahdslashklhsad')
    assert x == "OXGBLSVSLIBZMMEEMRKE"

def test_Rotor_init():
    rotor1 = Rotor('I','Q', next_rotor = None, prev_rotor = None)
    rotor2 = Rotor('II', 'a', next_rotor=rotor1, prev_rotor=None)
    rotor3 = Rotor('III', 'a', next_rotor=None, prev_rotor=rotor1)
    rotor1.step()
    rotor2.step()
    rotor3.step()

def test_multiple_init():
    enigma = Enigma(key='ABC', swaps=[('A', 'B'),('C', 'B')], rotor_order=['II', 'I', 'III'])
    x = enigma.encipher('jsksdhahdslashklhsad')
    assert x == "OXGBLSVSLIBZMMEEMRKE"
    enigma2 = Enigma(key='ABC', swaps=[('A', 'B'), ('C', 'B')], rotor_order=['II', 'I', 'III'])
    x = enigma2.encipher('jsksdhahdslashklhsad')
    assert x == "OXGBLSVSLIBZMMEEMRKE"

def test_multiple_init2():
    enigma = Enigma(key='ABC', swaps=[('A', 'B'),('C', 'B')], rotor_order=['II', 'I', 'III'])
    x = enigma.encipher('jsksdhahdslashklhsad')
    assert x == "OXGBLSVSLIBZMMEEMRKE"
    x = enigma.encipher('jsksdhahdslashklhsad')
    assert x == "KEIBLGMFLHYDDDXCDGTU"

def test_multiple_init3():
    enigma = Enigma(key='ABC', swaps=[('A', 'B'),('C', 'D')], rotor_order=['II', 'I', 'III'])
    x = enigma.encipher('abcd')
    assert x == "HYOS"
    enigma2 = Enigma(key='ABC', swaps=[('A', 'B'), ('C', 'D')], rotor_order=['II', 'I', 'III'])
    x = enigma2.decipher('HYOS')
    assert x == "ABCD"

def test_multiple_init4():
    enigma = Enigma(key='ABC', swaps=[('A', 'B'),('C', 'D')], rotor_order=['II', 'I', 'III'])
    x = enigma.encipher('jsksdhahdslashklhsad')
    assert x == "OXGDZSVSIIDZMMEEMRKZ"
    enigma2 = Enigma(key='ABC', swaps=[('A', 'B'), ('C', 'E')], rotor_order=['II', 'I', 'III'])
    x = enigma2.encipher('jsksdhahdslashklhsad')
    assert x == "OXGELSVSLIEZMMCCMRKC"


def test_multiple_init5():
    enigma = Enigma(key='ZZZ', swaps=[('K', 'L'), ('x', 'y'), ('a', 'Z'), ('n', 'M')], rotor_order=['V', 'I', 'III'])
    enigma = Enigma(key='ZZZ', swaps=[('K', 'L'), ('x', 'y'), ('a', 'Z'), ('n', 'M')], rotor_order=['V', 'I', 'III'])
    string = 'abcdefg  hijklmnopqrstuvwxyz'
    mul_string = string * 30
    x = enigma.encipher(mul_string)
    assert x == "HKHBaIRSFSJIUXXGOAFEDTKHnDGQRJUPSQJaVCBAYNKKCXNIYADJO"\
"VVHIROCUVNTLXFLNIHWTDVKEYLAnCLKFaPKPFnEQRVJXWXnIGDCEXVQVORNQHGKIBUWOVHULHURAKNRJBYVHTBOSDROCDDPaESWQHKEWTEWUEJGa"\
"DXRWPIJKXEBHIaVUTVVGYJTOGVUXaWKIFSHEBTULYNWnHHnFUTSJTDJVAXHLKDIAaGAGaOnNPIPPLQSYTXONGGVCCYDIGBSSRPaVUJQTFUXTYYCT"\
"EaDSHDNBRWQABKCRODBBRYHVJOYnENQKKBJDKaWLRSGnQLnJYIRPSPBDnNQTXGRYRSTEnOAVCBWPIILaLSLRFCQKLKYRYPBVBWHDHAUWHKCFGIGN"\
"VDGaKVIRNRTXnWVUaOTEQWHLDKaCYPInLnLSWTNSYNCCDRIJRUACInCDnIYaCYUWJDXFSNONRaDOALBUKEGIUANaCCAOBUWXXBUDDPNNLSOXLKIC"\
"EDTaXaCSAUYVDQQNELGWKNCQKAQJAYRXAYJnKYaDFVSaGXGFNBNUGPUNQLVIQnJQBWKLLFVYQEENSYEaaFPGCSTRXGINSEWKYQKYRaEFRYCJYUPW"\
"SXOOWDTCVTTSaGEJKVANXBXYLDXRUADCUTBOQRQKQGWDDAHDSVaBWaCKUNEXRDTNEGPYICDOSaDaDBGILHPVWUSaHFaFNBYBaNBWGDHQQDUQKCKC"\
"PFOOVKIOLOAODATATDXILTGTPJCNFJTOIHLXPnTLEJKnKESJAHADNIY"


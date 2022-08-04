"""
使い方　python midi_to_independent_instrument_midi.py midifileの入っているfolderのpath/**　楽器ごとに分けたmidiファイルが全部入るfolder名　
例      python midi_to_independent_instrument_midi.py midiget/saved_midi_vgmusic output
    
"""
import pretty_midi
import os
import sys
import glob
def midi_to_inst_midi(input_dir,output_dir):
    # outputディレクトリがなければ作成
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    for file in files:
        file_name=file.split("/")[-1].split(".")[0]
        print(file_name)
        midi_data=pretty_midi.PrettyMIDI(file)
        # 該当曲のディレクトリを作成
        if not os.path.isdir(output_dir+'/' + str(file_name)):
            os.mkdir(output_dir+'/' + str(file_name))
        # 楽器を1つ1つ取り出し、インスタンスにする
        for i in range(0,len(midi_data.instruments)):
            """
            instrument:変数は以下　
            楽器番号program(int),
            ドラムかどうかのis_drum(bool),
            楽器名name(str),
            音符notes(list[velocity, pitch, start, end]),
            音高曲げ量とタイミングpitch_bends(list[pitch, time]),
            コントロール機能番号とデータ値control_changes(list[number, value, time]) 
            例1 Instrument(program=11, is_drum=True, name="Track 4")
            例2 Instrument(program=62, is_drum=False, name="Melody")
            
            instrument_name:楽器名はmidi製作者が入れているので、たまにgmailアドレスが入っていたりright_handとかStaff-1とか楽器名じゃないものも入っている。
            例 Track 4, Melody, Drum, Guiter
            program_num:楽器番号
            例 0, 11, 62, 89 
            """
            instrument = midi_data.instruments[i]  
            instrument_name = midi_data.instruments[i].name
            program_num = midi_data.instruments[i].program     
            # 新規作成用のPrettyMIDIオブジェクトを作る
            rev_en_chord = pretty_midi.PrettyMIDI()
            # instrumentをPrettyMIDIオブジェクトに追加
            rev_en_chord.instruments.append(instrument)
            # 保存する
            rev_en_chord.write(output_dir+'/'+str(file_name) + '/' + str(file_name) +'_ins_' + str(program_num) +'_'+str(instrument_name)+ '.mid')


def check_no_args(arguments):
    """ Check that user has input at least 1 argument"""
    
    if len(arguments) < 2:
        print()
        print("At least 1 argument (i.e., start page) must be provided.")
        print()
        sys.exit(0)
        
if __name__ == "__main__":
    #使い方　python midi_to_independent_instrument_midi.py midifileの入っているfolderのpath/**　楽器ごとに分けたmidiファイルが全部入るfolder名　
    #例      python midi_to_independent_instrument_midi.py midiget/saved_midi_vgmusic output
    
    # check args are ok
    check_no_args(sys.argv)
    #input_dirにmidifileの入っているfolderのpath/**を入れます
    input_dir = sys.argv[1]+"/**"
    #output_dirに楽器ごとに分けたmidiファイルが全部入るfolder名を指定します
    output_dir =sys.argv[2]
    files = glob.glob(input_dir)
    midi_to_inst_midi(input_dir,output_dir)
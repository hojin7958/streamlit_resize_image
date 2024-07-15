from PIL import Image
import io
import streamlit as st
import streamlit_ext as ste

st.set_page_config(page_title="MMS발송용 이미지 사이즈 품질 변환기")


st.header("이미지 사이즈 변환기 (24.7월까지만 운영)")
st.subheader("이미지가 최대 70kb를 초과하지 않도록 조절해드려요")
st.write("이미지 가로사이즈 800px로 고정한뒤 70Kb에 맞추도록 이미지 품질을 조정합니다")

st.warning("""
           24.8월부터 이미지 변환기 사이트 주소를 변경해요  
           
           https://bohumin.co.kr/tools/resize70
           """)

st.info("""
        가족간병, 간병인신청할때에는 심플케어  
        https://simplecare.kr        
           """)


st.write("")
st.markdown("---")

uploaded_file = st.file_uploader("리플렛 파일을 업로드해주세요", type=['png','jpg','jpeg'])


if uploaded_file:
    img = Image.open(uploaded_file)
    img = img.convert("RGB")

    basewidth = 800
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)

    out = io.BytesIO()
    img.save(out, format='jpeg', quality=100)
    out.tell()/1024

    quality = 100
    output_size = 100

    while output_size>=70:
        quality = quality-1
    #     print("시작", quality)
        out = io.BytesIO()
        img.save(out, format='jpeg', quality=quality)
        output_size = out.tell()/1024
        # print(output_size,quality)


    img.save('temp800.jpg', format='jpeg', quality=quality)

    st.write(output_size)


    with open("temp800.jpg", "rb") as file:
        btn = ste.download_button(
                label="이미지다운로드를 하려면 이곳을 클릭",
                data=file,
                file_name="temp800.jpg",
                mime="image/jpg"
            )

    st.image(img)

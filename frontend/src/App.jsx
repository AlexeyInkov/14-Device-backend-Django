import {useState} from "react";
import './App.css'
import {Header} from "./components/Header.jsx";
import {Menu} from "./components/Menu.jsx";
import {Addresses} from "./components/Addresses.jsx";
import {Devices} from "./components/Devices.jsx";


function App() {

    const [tsoId, setTsoId] = useState(null);
    const [customerId, setCustomerId] = useState(null);
    const [meteringUnitId, setMeteringUnitId] = useState(null);

    const resetState = () => {
        setTsoId(null);
        setCustomerId(null);
        setMeteringUnitId(null);
    }

    return (
        <div className="App">
            <Header/>
            <div className="wrapper">
                <aside>
                    <div className="window">
                        <p className="tso" onClick={resetState}>TCO</p>
                        <Menu setTsoId={setTsoId} setCustomerId={setCustomerId} setMeteringUnitId={setMeteringUnitId} className="menu"/>
                    </div>
                </aside>
                <article>
                    <section className="address">
                        <Addresses tsoId={tsoId} customerId={customerId} setMeteringUnitId={setMeteringUnitId}
                                   className="addresses"/>
                    </section>
                    <section className="device">
                        <Devices meteringUnitId={meteringUnitId} className="addresses"/>

                    </section>
                </article>
            </div>

            {/*<Footer/>*/}
        </div>
    );
}

export default App;

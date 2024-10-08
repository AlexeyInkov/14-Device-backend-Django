import '../styles/header.css';


function Header(props) {
    const {userData} = props;
    return (
        <header>
            <div>Контроль поверок приборов</div>
            <nav className="navigat">
                <div>ЗАО НТО ГАЛАКС</div>
            </nav>
            <div>
                {
                    userData ? (
                        <div>
                            {userData.username}
                            <input type={"button"} value={"logout"}/>
                        </div>
                    ) : (
                        <form>
                            <input type="text" placeholder="login:"/>
                            <input type="password" placeholder="password:"/>
                            <input type={"button"} value={"login"}/>
                        </form>
                    )
                }
            </div>

        </header>);
}

export {Header};
import React, { ReactNode } from "react"
import {
  ComponentProps,
  StreamlitComponentBase,
  Streamlit,
  withStreamlitConnection,
} from "./streamlit"
import "./Tab.css"

interface State {
  activeTab: string
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class Tabs extends StreamlitComponentBase<State> {
  public constructor(props: ComponentProps) {
    super(props)

    const tabs = this.props.args["tabs"] || ['Safety', 'Metrics']

    this.state = {
      activeTab: tabs[0]
    }
    Streamlit.setComponentValue(this.state.activeTab)
  }

  public render = (): ReactNode => {
    const tabs = this.props.args["tabs"]

    return (
      <div className="tabs">
        {tabs.map((tab: string) => (
          <button
            onClick={this.onClicked}
            id={tab}
            className={ `tabs__tab ${this.state.activeTab === tab ? 'tabs__tab--active' : ''}`}
          >
            { tab }
          </button>
        ))}
      </div>
    )
  }

  private onClicked = (event: React.MouseEvent<HTMLElement>): void => {
    console.log(event.currentTarget.id)
    this.setState({ activeTab: event.currentTarget.id })
    Streamlit.setComponentValue(event.currentTarget.id)
  }
}

export default withStreamlitConnection(Tabs)
